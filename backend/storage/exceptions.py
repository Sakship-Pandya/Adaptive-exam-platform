from rest_framework.exceptions import APIException


class StorageException(APIException):
    status_code = 500
    default_detail = "A storage operation failed."
    default_code = "storage_error"


class StorageConnectionException(StorageException):
    status_code = 503
    default_detail = "Unable to connect to the storage provider."
    default_code = "storage_connection_failed"


class BucketNotFoundException(StorageException):
    status_code = 404
    default_detail = "The configured storage bucket could not be found."
    default_code = "bucket_not_found"


class BucketCreationException(StorageException):
    status_code = 500
    default_detail = "Failed to create the storage bucket."
    default_code = "bucket_creation_failed"


class ObjectNotFoundException(StorageException):
    status_code = 404
    default_detail = "The requested object could not be found."
    default_code = "object_not_found"


class ObjectVerificationException(StorageException):
    status_code = 400
    default_detail = "The uploaded object failed verification."
    default_code = "object_verification_failed"


class PresignedURLException(StorageException):
    status_code = 500
    default_detail = "Unable to generate a pre-signed URL."
    default_code = "presigned_url_generation_failed"


class ObjectDeletionException(StorageException):
    status_code = 500
    default_detail = "Failed to delete the object from storage."
    default_code = "object_deletion_failed"