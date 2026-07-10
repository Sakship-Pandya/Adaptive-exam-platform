from rest_framework import status
from rest_framework.exceptions import APIException


class FileException(APIException):
    """
    Base exception for all file-related operations.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A file operation failed."
    default_code = "file_error"


# ==========================================================
# Upload Session Exceptions
# ==========================================================


class UploadSessionCreationException(FileException):
    """
    Raised when an upload session cannot be created.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to create the upload session."
    default_code = "upload_session_creation_failed"


class UploadSessionNotFoundException(FileException):
    """
    Raised when the requested upload session does not exist.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested upload session could not be found."
    default_code = "upload_session_not_found"


class UploadSessionExpiredException(FileException):
    """
    Raised when an upload session has expired.
    """

    status_code = status.HTTP_410_GONE
    default_detail = "The upload session has expired."
    default_code = "upload_session_expired"


class UploadSessionCompletedException(FileException):
    """
    Raised when an operation is attempted on a completed upload session.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "The upload session has already been completed."
    default_code = "upload_session_completed"


class UploadSessionFailedException(FileException):
    """
    Raised when an operation is attempted on a failed upload session.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "The upload session has already failed."
    default_code = "upload_session_failed"


class UploadSessionVerificationException(FileException):
    """
    Raised when one or more uploaded files fail verification.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "One or more uploaded files failed verification."
    default_code = "upload_session_verification_failed"


class UploadSessionCleanupException(FileException):
    """
    Raised when uploaded objects cannot be cleaned up after a failed upload.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to clean up uploaded objects."
    default_code = "upload_session_cleanup_failed"


class UploadSessionStateException(FileException):
    """
    Raised when an upload session is in an invalid state for the requested operation.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "The upload session is in an invalid state."
    default_code = "upload_session_invalid_state"


class UploadSessionCompletionException(FileException):
    """
    Raised when an upload session cannot be marked as completed.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to complete the upload session."
    default_code = "upload_session_completion_failed"


# ==========================================================
# Upload Verification Exceptions
# ==========================================================


class UploadedObjectNotFoundException(FileException):
    """
    Raised when an expected uploaded object does not exist in object storage.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "The uploaded object could not be found."
    default_code = "uploaded_object_not_found"


class UploadedObjectSizeMismatchException(FileException):
    """
    Raised when the uploaded object's size differs from the expected size.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "The uploaded object's size does not match the expected size."
    default_code = "uploaded_object_size_mismatch"


class UploadedObjectContentTypeMismatchException(FileException):
    """
    Raised when the uploaded object's content type differs from the expected content type.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "The uploaded object's content type does not match the expected content type."
    default_code = "uploaded_object_content_type_mismatch"


class UploadedObjectIntegrityException(FileException):
    """
    Raised when an uploaded object's integrity verification fails.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "The uploaded object's integrity verification failed."
    default_code = "uploaded_object_integrity_failed"


# ==========================================================
# Permanent File Exceptions
# ==========================================================


class FileAlreadyExistsException(FileException):
    """
    Raised when a duplicate permanent file is detected.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "The file already exists."
    default_code = "file_already_exists"


class FileNotFoundException(FileException):
    """
    Raised when the requested permanent file cannot be found.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested file could not be found."
    default_code = "file_not_found"


class FilePermissionException(FileException):
    """
    Raised when the user does not have permission to access a file.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to access this file."
    default_code = "file_permission_denied"


class FileProcessingException(FileException):
    """
    Raised when a file cannot be processed.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An error occurred while processing the file."
    default_code = "file_processing_failed"


class DuplicateFileHashException(FileException):
    """
    Raised when a file with the same SHA-256 hash already exists.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "A file with the same content already exists."
    default_code = "duplicate_file_hash"