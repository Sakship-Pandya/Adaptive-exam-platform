from django.db import models
from common.models import BaseModel
from authentication.models import User
from common.choices import WorkspaceStatus

class Workspace(BaseModel):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workspaces"
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=WorkspaceStatus.choices,
        default=WorkspaceStatus.EMPTY
    )

    processing_signature = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    last_processed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "title"],
                name="unique_workspace_title_per_user",
            )
        ]
        ordering = ["-created_at"]