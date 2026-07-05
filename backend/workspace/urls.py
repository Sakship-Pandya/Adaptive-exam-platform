from django.urls import path

from .views import CreateWorkspaceView,UpdateWorkspaceView,DeleteWorkspaceView

urlpatterns = [
    path(
        "create/",
        CreateWorkspaceView.as_view(),
        name="create-workspace",
    ),
    path(
        "<uuid:workspace_id>/",
        UpdateWorkspaceView.as_view(),
        name="update-workspace",
    ),
    path(
        "<uuid:workspace_id>/delete/",
        DeleteWorkspaceView.as_view(),
        name="delete-workspace",
    ),
]