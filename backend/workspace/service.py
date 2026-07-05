from django.db import IntegrityError, transaction

from workspace.models import Workspace
from workspace.exceptions import (
    WorkspaceCreationException,
    WorkspaceAlreadyExistsException,
    WorkspaceNotFoundException,
    WorkspacePermissionException,
    WorkspaceArchivedException,
    WorkspaceUpdateException,
    WorkspaceDeletionException
)
from common.choices import WorkspaceStatus

class WorkspaceService:

    @staticmethod
    @transaction.atomic
    def create_workspace(*, owner, title, description=""):
        try:
            workspace = Workspace.objects.create(
                owner=owner,
                title=title,
                description=description,
            )

            return workspace

        except IntegrityError as exc:
            exc_str = str(exc).lower()
            if "unique" in exc_str or "duplicate" in exc_str:
                raise WorkspaceAlreadyExistsException() from exc

            raise WorkspaceCreationException(
                "Unable to create workspace."
            ) from exc
    

    @staticmethod
    @transaction.atomic
    def update_workspace(
        *,
        workspace_id,
        owner,
        title=None,
        description=None,
    ):
        try:
            workspace = Workspace.objects.get(id=workspace_id)

        except Workspace.DoesNotExist as exc:
            raise WorkspaceNotFoundException() from exc

        if workspace.owner != owner:
            raise WorkspacePermissionException()

        if workspace.status == WorkspaceStatus.ARCHIVED:
            raise WorkspaceArchivedException()

        if title is not None:
            workspace.title = title

        if description is not None:
            workspace.description = description

        try:
            workspace.save(update_fields=["title", "description", "updated_at"])
            return workspace

        except IntegrityError as exc:
            exc_str = str(exc).lower()

            if "unique" in exc_str or "duplicate" in exc_str:
                raise WorkspaceAlreadyExistsException() from exc

            raise WorkspaceUpdateException() from exc
    

    @staticmethod
    @transaction.atomic
    def delete_workspace(
        *,
        workspace_id,
        owner,
    ):
        try:
            workspace = Workspace.objects.select_for_update().get(id=workspace_id)

        except Workspace.DoesNotExist as exc:
            raise WorkspaceNotFoundException() from exc

        if workspace.owner != owner:
            raise WorkspacePermissionException()

        if workspace.status == WorkspaceStatus.ARCHIVED:
            raise WorkspaceArchivedException()

        try:
            workspace.delete()

        except Exception as exc:
            raise WorkspaceDeletionException() from exc