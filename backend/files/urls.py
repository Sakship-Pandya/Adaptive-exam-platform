from django.urls import path

from files.views import CreateUploadSessionView, FinalizeUploadView

app_name = "files"

urlpatterns = [
    path(
        "upload-request/",
        CreateUploadSessionView.as_view(),
        name="create-upload-session",
    ),
    path(
        "upload-request/finalize/",
        FinalizeUploadView.as_view(),
        name="finalize-upload",
    ),
]