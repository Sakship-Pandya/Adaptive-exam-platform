from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError, IntegrityError, transaction
from django.utils import timezone

from common.choices import UploadSessionStatus, UploadFileStatus
from files.exceptions import (
    FileException,
    UploadedObjectContentTypeMismatchException,
    UploadedObjectIntegrityException,
    UploadedObjectNotFoundException,
    UploadedObjectSizeMismatchException,
    UploadSessionCleanupException,
    UploadSessionCompletionException,
    UploadSessionCreationException,
    UploadSessionVerificationException,
    UploadSessionNotFoundException,
    UploadSessionExpiredException,
    UploadSessionCompletedException,
    UploadSessionFailedException,
    UploadSessionStateException,
)

from files.models import UploadSession, UploadSessionFile
from storage.provider import MinIOProvider
from storage.utils import generate_storage_key


class FilesService:
    """
    Service responsible for orchestrating the upload workflow.

    This service coordinates:
        - Upload session creation.
        - Temporary upload file records.
        - Storage key generation.
        - Pre-signed URL generation.

    It does NOT:
        - Verify uploaded files.
        - Create permanent File records.
        - Calculate file hashes.
        - Delete failed uploads.

    Those operations belong to the upload finalization stage.
    """

    provider = MinIOProvider()

    @staticmethod
    @transaction.atomic
    def create_upload_session(
        *,
        workspace,
        user,
        files: list[dict],
    ) -> dict:
        """
        Create an upload session and generate upload instructions.

        Args:
            workspace:
                Workspace receiving the uploaded files.

            user:
                User initiating the upload.

            files:
                List of validated file metadata.

        Returns:
            Dictionary containing upload session information and
            pre-signed upload URLs.
        """

        try:
            expected_total_size = sum(
                file["size"] for file in files
            )

            upload_session = UploadSession.objects.create(
                workspace=workspace,
                user=user,
                status=UploadSessionStatus.PENDING,
                expected_file_count=len(files),
                expected_total_size=expected_total_size,
                expires_at=timezone.now()
                + timedelta(
                    seconds=settings.UPLOAD_SESSION_EXPIRY_SECONDS
                ),
            )

            upload_files = []

            for file in files:

                storage_key = generate_storage_key(
                    workspace_id=workspace.id,
                    upload_session_id=upload_session.id,
                    file_role=file["role"],
                    filename=file["filename"],
                )

                upload_session_file = UploadSessionFile.objects.create(
                    upload_session=upload_session,
                    original_filename=file["filename"],
                    storage_key=storage_key,
                    role=file["role"],
                    status=UploadFileStatus.PENDING,
                    expected_file_size=file["size"],
                    expected_content_type=file["content_type"],
                )

                upload_url = FilesService.provider.generate_upload_url(
                    storage_key=storage_key,
                    content_type=file["content_type"],
                )

                upload_files.append(
                    {
                        "upload_session_file_id": upload_session_file.id,
                        "original_filename": file["filename"],
                        "role": file["role"],
                        "storage_key": storage_key,
                        "content_type": file["content_type"],
                        "expected_file_size": file["size"],
                        "upload_url": upload_url,
                    }
                )

            return {
                "upload_session_id": upload_session.id,
                "expires_at": upload_session.expires_at,
                "files": upload_files,
            }

        except IntegrityError as exc:
            raise UploadSessionCreationException(
                detail="Failed to create upload session."
            ) from exc

        except DatabaseError as exc:
            raise UploadSessionCreationException(
                detail="Database error occurred while creating the upload session."
            ) from exc

        except Exception as exc:
            raise FileException(
                detail="Unexpected error occurred while creating the upload session."
            ) from exc

    @staticmethod
    @transaction.atomic
    def finalize_upload(upload_session_id, user):
        """
        Finalize an upload session.

        Workflow
        --------
        1. Retrieve and lock the upload session.
        2. Validate the upload session.
        3. Verify every uploaded object.
        4. Mark the upload session as completed.
        5. Return a summary of the completed upload session.

        Any verification failure causes the upload session to be rolled back.
        """

        upload_session = FilesService._get_upload_session(
            upload_session_id=upload_session_id,
            user=user,
        )
        FilesService._verify_upload_session(
            upload_session=upload_session,
        )

        try:
            upload_session.status = UploadSessionStatus.VERIFYING
            upload_session.save(update_fields=["status"])
        except DatabaseError as exc:
            raise UploadSessionStateException(
                detail="Failed to update upload session status to VERIFYING."
            ) from exc

        try:
            FilesService._verify_uploaded_objects(
                upload_session=upload_session,
            )

        except (
            UploadSessionVerificationException,
            UploadedObjectNotFoundException,
            UploadedObjectSizeMismatchException,
            UploadedObjectContentTypeMismatchException,
            UploadedObjectIntegrityException,
        ) as verification_exception:

            try:
                FilesService._fail_upload_session(
                    upload_session=upload_session,
                    failure_reason=str(verification_exception),
                )

            except (UploadSessionStateException, DatabaseError):
                # Log here: session failure cleanup itself failed.
                pass

            raise verification_exception

        FilesService._complete_upload_session(
            upload_session=upload_session,
        )

        upload_session.refresh_from_db()

        return {
            "upload_session_id": upload_session.id,
            "status": upload_session.status,
            "verified_file_count": upload_session.uploaded_file_count,
            "completed_at": upload_session.completed_at,
        }

    @staticmethod
    def _get_upload_session(upload_session_id, user):
        """
        Retrieve and lock an upload session belonging to the authenticated user.

        The upload session is locked using SELECT FOR UPDATE to prevent
        concurrent finalization requests.

        Raises
        ------
        UploadSessionNotFoundException
            If the upload session does not exist or does not belong to the user.
        """

        try:
            return (
                UploadSession.objects
                .select_for_update()
                .select_related("workspace")
                .get(
                    id=upload_session_id,
                    user=user,
                )
            )

        except ObjectDoesNotExist as exc:
            raise UploadSessionNotFoundException() from exc

    @staticmethod
    def _verify_upload_session(upload_session):
        """
        Validate that the upload session is eligible for finalization.

        Checks
        ------
        - Upload session has not expired.
        - Upload session is not already completed.
        - Upload session is not already failed.
        - Upload session is in the expected state.

        Raises
        ------
        UploadSessionExpiredException
        UploadSessionCompletedException
        UploadSessionFailedException
        UploadSessionStateException
        """
        if upload_session.expires_at <= timezone.now():
            raise UploadSessionExpiredException()

        if upload_session.status == UploadSessionStatus.COMPLETED:
            raise UploadSessionCompletedException()

        if upload_session.status == UploadSessionStatus.FAILED:
            raise UploadSessionFailedException()

        if upload_session.status != UploadSessionStatus.PENDING:
            raise UploadSessionStateException()

    @staticmethod
    def _verify_uploaded_objects(upload_session):
        """
        Verify every uploaded object belonging to the upload session.

        This method performs verification in two phases:

        Phase 1
        -------
        Validate every uploaded object against object storage.

        Phase 2
        -------
        Persist verification metadata for every successfully verified object.

        Raises
        ------
        UploadSessionVerificationException
        """

        upload_session_files = FilesService._get_upload_session_files(
            upload_session=upload_session,
        )

        verified_objects = []

        for upload_session_file in upload_session_files:

            metadata = FilesService.provider.get_object_metadata(
                storage_key=upload_session_file.storage_key,
            )

            FilesService._verify_uploaded_object(
                upload_session_file=upload_session_file,
                metadata=metadata,
            )

            verified_objects.append(
                (
                    upload_session_file,
                    metadata,
                )
            )

        for upload_session_file, metadata in verified_objects:

            FilesService._update_upload_session_file(
                upload_session_file=upload_session_file,
                metadata=metadata,
            )

    @staticmethod
    def _verify_uploaded_object(upload_session_file, metadata):
        """
        Verify that an uploaded object's metadata matches the expected metadata.

        Parameters
        ----------
        upload_session_file : UploadSessionFile
            Upload session file containing the expected metadata.

        metadata : dict
            Normalized metadata returned by the storage provider.

        Raises
        ------
        UploadedObjectIntegrityException
            If the uploaded object is empty or contains invalid metadata.

        UploadedObjectSizeMismatchException
            If the uploaded object's size does not match the expected size.

        UploadedObjectContentTypeMismatchException
            If the uploaded object's content type does not match the expected
            content type.
        """

        content_length = metadata["content_length"]
        content_type = metadata["content_type"]

        if not isinstance(content_length, int):
            raise UploadedObjectIntegrityException()

        if content_length <= 0:
            raise UploadedObjectIntegrityException()

        expected_content_type = (
            upload_session_file.expected_content_type
            .split(";")[0]
            .strip()
            .lower()
        )

        uploaded_content_type = (
            content_type
            .split(";")[0]
            .strip()
            .lower()
        )

        if content_length != upload_session_file.expected_file_size:
            raise UploadedObjectSizeMismatchException()

        if uploaded_content_type != expected_content_type:
            raise UploadedObjectContentTypeMismatchException()

    @staticmethod
    def _get_upload_session_files(upload_session):
        """
        Retrieve all UploadSessionFile records belonging to an upload session.

        Raises
        ------
        UploadSessionVerificationException
            If the upload session does not contain any associated files.
        """

        upload_session_files = (
            UploadSessionFile.objects
            .filter(upload_session=upload_session)
            .order_by("created_at")
        )

        if not upload_session_files.exists():
            raise UploadSessionVerificationException(
                detail="The upload session does not contain any files."
            )
        return upload_session_files

    @staticmethod
    def _update_upload_session_file(upload_session_file, metadata):
        """
        Persist verified metadata for an uploaded object.

        Parameters
        ----------
        upload_session_file : UploadSessionFile
            The upload session file to update.

        metadata : dict
            Normalized object metadata returned by the storage provider.
        """

        upload_session_file.uploaded_file_size = metadata["content_length"]
        upload_session_file.uploaded_content_type = metadata["content_type"]
        upload_session_file.etag = metadata["etag"]
        upload_session_file.object_last_modified = metadata["last_modified"]

        upload_session_file.verified_at = timezone.now()
        upload_session_file.status = UploadFileStatus.VERIFIED
        try:
            upload_session_file.save(
                update_fields=[
                    "uploaded_file_size",
                    "uploaded_content_type",
                    "etag",
                    "object_last_modified",
                    "verified_at",
                    "status",
                    "updated_at",
                ]
            )
        except DatabaseError as exc:
            raise UploadSessionVerificationException(
                detail="Failed to persist verified metadata to the database."
            ) from exc

    @staticmethod
    def _fail_upload_session(upload_session, failure_reason):
        """
        Roll back an upload session.

        Workflow
        --------
        1. Delete uploaded objects from storage.
        2. Mark UploadSessionFile records as failed.
        3. Mark UploadSession as failed.
        """

        upload_session_files = UploadSessionFile.objects.filter(
            upload_session=upload_session,
        )

        for session_file in upload_session_files:
            try:
                FilesService.provider.delete_object(
                    storage_key=session_file.storage_key,
                )
            except Exception:
                # Storage deletion failure is non-fatal during rollback.
                # The object may not have been uploaded yet.
                pass

        FilesService._mark_upload_session_files_failed(
            upload_session=upload_session,
            failure_reason=failure_reason,
        )

        FilesService._mark_upload_session_failed(
            upload_session=upload_session,
        )

    @staticmethod
    def _mark_upload_session_files_failed(upload_session, failure_reason):
        """
        Mark every non-verified UploadSessionFile in the upload session as failed.

        Files that have already been verified are left unchanged.
        Files that do not already have a failure reason are updated with the
        provided failure_reason.
        """

        (
            UploadSessionFile.objects
            .filter(
                upload_session=upload_session,
            )
            .exclude(
                status=UploadFileStatus.VERIFIED,
            )
            .update(
                status=UploadFileStatus.FAILED,
                failure_reason=failure_reason,
            )
        )

    @staticmethod
    def _mark_upload_session_failed(upload_session):
        """
        Mark the upload session as failed.

        Updates
        -------
        - status
        """

        try:
            upload_session.status = UploadSessionStatus.FAILED

            upload_session.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        except DatabaseError as exc:
            raise UploadSessionStateException(
                detail="Failed to mark the upload session as failed."
            ) from exc

    @staticmethod
    def _complete_upload_session(upload_session):
        """
        Mark an upload session as successfully completed.

        Updates
        -------
        - status
        - completed_at
        - uploaded_file_count
        """

        try:
            upload_session.status = UploadSessionStatus.COMPLETED
            upload_session.completed_at = timezone.now()
            upload_session.uploaded_file_count = (
                UploadSessionFile.objects.filter(
                    upload_session=upload_session,
                    status=UploadFileStatus.VERIFIED,
                ).count()
            )

            upload_session.save(
                update_fields=[
                    "status",
                    "completed_at",
                    "uploaded_file_count",
                    "updated_at",
                ]
            )

        except DatabaseError as exc:
            raise UploadSessionCompletionException(
                "Failed to complete the upload session."
            ) from exc
