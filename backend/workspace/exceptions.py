from rest_framework import status
from rest_framework.exceptions import APIException


class WorkspaceException(APIException):
    """Base exception for all workspace-related errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "workspace_error"
    default_detail = "An unknown workspace error occurred."


class WorkspaceCreationException(WorkspaceException):
    """Raised when a workspace cannot be created."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "workspace_creation_failed"
    default_detail = "Unable to create the workspace."


class WorkspaceNotFoundException(WorkspaceException):
    """Raised when the requested workspace does not exist."""
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "workspace_not_found"
    default_detail = "The requested workspace does not exist."


class WorkspacePermissionException(WorkspaceException):
    """Raised when a user attempts to access a workspace they do not own."""
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "workspace_permission_denied"
    default_detail = (
        "You do not have permission to perform this action on this workspace."
    )


class WorkspaceProcessingException(WorkspaceException):
    """Raised when workspace processing fails."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "workspace_processing_failed"
    default_detail = "An error occurred while processing the workspace."


class InvalidWorkspaceStateException(WorkspaceException):
    """Raised when an operation is attempted in an invalid workspace state."""
    status_code = status.HTTP_409_CONFLICT
    default_code = "invalid_workspace_state"
    default_detail = "The workspace is in an invalid state for this operation."


class WorkspaceAlreadyExistsException(WorkspaceException):
    """Raised when a duplicate workspace cannot be created."""
    status_code = status.HTTP_409_CONFLICT
    default_code = "workspace_already_exists"
    default_detail = "A workspace with the same name already exists."


class WorkspaceValidationException(WorkspaceException):
    """Raised when workspace validation fails."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "workspace_validation_failed"
    default_detail = "Workspace validation failed."


class WorkspaceFileRequirementException(WorkspaceException):
    """Raised when required files are missing from a workspace."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "workspace_file_requirement_failed"
    default_detail = (
        "The required files have not been uploaded to the workspace."
    )


class WorkspaceCoverageException(WorkspaceException):
    """Raised when workspace topic coverage is below the required threshold."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "workspace_coverage_insufficient"
    default_detail = (
        "The uploaded notes do not sufficiently cover the topics in the question bank."
    )


class WorkspaceArchivedException(WorkspaceException):
    """Raised when an operation is attempted on an archived workspace."""
    status_code = status.HTTP_409_CONFLICT
    default_code = "workspace_archived"
    default_detail = "The workspace has been archived and cannot be modified."


class WorkspaceDeletionException(WorkspaceException):
    """Raised when a workspace cannot be deleted."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "workspace_deletion_failed"
    default_detail = "Unable to delete the workspace."


class WorkspaceUpdateException(WorkspaceException):
    """Raised when a workspace cannot be updated."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "workspace_update_failed"
    default_detail = "Unable to update the workspace."


class WorkspaceProcessingInProgressException(WorkspaceException):
    """Raised when an operation cannot proceed because processing is already running."""
    status_code = status.HTTP_409_CONFLICT
    default_code = "workspace_processing_in_progress"
    default_detail = (
        "The workspace is currently being processed. Please wait until processing completes."
    )


class WorkspaceNotReadyException(WorkspaceException):
    """Raised when an operation requires a processed workspace."""
    status_code = status.HTTP_409_CONFLICT
    default_code = "workspace_not_ready"
    default_detail = (
        "The workspace is not ready for this operation. Complete processing first."
    )