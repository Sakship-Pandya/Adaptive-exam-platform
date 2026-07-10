import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, EndpointConnectionError
from decouple import config

from storage.exceptions import (
    BucketCreationException,
    BucketNotFoundException,
    ObjectNotFoundException,
    PresignedURLException,
    StorageConnectionException,
    StorageException,
)

class MinIOProvider:
    """
    Low-level storage provider responsible for communicating directly with
    the S3-compatible object storage (MinIO).

    This class should be the only component that communicates directly
    with boto3. Higher layers (StorageService) should use this provider
    instead of interacting with boto3 themselves.
    """

    def __init__(self):
        self.endpoint = config("MINIO_ENDPOINT")
        self.access_key = config("MINIO_ACCESS_KEY")
        self.secret_key = config("MINIO_SECRET_KEY")
        self.bucket_name = config("MINIO_BUCKET")
        self.region = config("MINIO_REGION", default="us-east-1")

        self.use_ssl = (
            config("MINIO_SECURE", default="False")
            .strip()
            .lower()
            == "true"
        )

        self._client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
            use_ssl=self.use_ssl,
            config=Config(signature_version="s3v4"),
        )

    def health_check(self) -> bool:
        """
        Verify that the storage service is reachable.

        Returns:
            bool: True if the connection succeeds.

        Raises:
            StorageConnectionException
        """
        try:
            self._client.list_buckets()
            return True

        except EndpointConnectionError as exc:
            raise StorageConnectionException(
                detail="Unable to connect to the storage provider."
            ) from exc

        except ClientError as exc:
            raise StorageConnectionException(
                detail="Storage provider returned an unexpected response."
            ) from exc

    def bucket_exists(self) -> bool:
        """
        Check whether the configured bucket exists.

        Returns:
            bool: True if the bucket exists, otherwise False.

        Raises:
            StorageConnectionException
        """
        try:
            self._client.head_bucket(Bucket=self.bucket_name)
            return True

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]

            if error_code in ("404", "NoSuchBucket", "NotFound"):
                return False

            raise StorageConnectionException(
                detail="Unexpected error while checking bucket existence."
            ) from exc

    def create_bucket(self) -> None:
        """
        Create the configured bucket if it does not already exist.

        Raises:
            BucketCreationException
        """
        try:
            if self.bucket_exists():
                return

            self._client.create_bucket(Bucket=self.bucket_name)

        except ClientError as exc:
            raise BucketCreationException(
                detail=f"Unable to create bucket '{self.bucket_name}'."
            ) from exc

    def ensure_bucket_exists(self) -> None:
        """
        Ensure that the configured bucket exists.

        If the bucket does not exist, it will be created.

        Raises:
            BucketNotFoundException
        """
        if self.bucket_exists():
            return

        self.create_bucket()

        if not self.bucket_exists():
            raise BucketNotFoundException(
                detail=f"Bucket '{self.bucket_name}' does not exist."
            )
    
    def generate_upload_url(
        self,
        storage_key: str,
        content_type: str,
        expires_in: int = 900,
    ) -> str:
        """
        Generate a pre-signed URL for uploading an object directly to MinIO.

        The backend never receives the file contents. Instead, it generates
        a temporary URL which the frontend uses to upload the file directly
        to the object storage service.

        Args:
            storage_key:
                Destination object key inside the bucket.

            content_type:
                Expected MIME type of the uploaded object.

            expires_in:
                Number of seconds before the URL expires.

        Returns:
            A pre-signed PUT URL.
        """

        try:
            return self._client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": storage_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )

        except ClientError as exc:
            raise PresignedURLException(
                detail="Failed to generate upload URL."
            ) from exc

    def get_object_metadata(
        self,
        storage_key: str,
    ) -> dict:
        """
        Retrieve metadata for an object stored in MinIO.

        This method is primarily used during upload verification to
        confirm that an uploaded object exists and matches the expected
        metadata.

        Args:
            storage_key:
                Object key inside the bucket.

        Returns:
            Dictionary containing the object's metadata.
        """

        try:
            response = self._client.head_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )

            return {
                "content_length": response["ContentLength"],
                "content_type": response["ContentType"],
                "etag": response["ETag"].strip('"'),
                "last_modified": response["LastModified"],
            }

        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code in ("404", "NoSuchKey", "NotFound"):
                raise ObjectNotFoundException(
                    detail="The requested object does not exist."
                ) from exc

            raise StorageException(
                detail="Failed to retrieve object metadata."
            ) from exc

    def delete_object(
        self,
        storage_key: str,
    ) -> None:
        """
        Delete an object from the storage bucket.

        This method is used during upload session rollback to remove
        objects that were uploaded but ultimately failed verification.

        Args:
            storage_key:
                Object key inside the bucket.

        Raises:
            StorageException
        """

        try:
            self._client.delete_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )

        except ClientError as exc:
            raise StorageException(
                detail="Failed to delete object from storage."
            ) from exc