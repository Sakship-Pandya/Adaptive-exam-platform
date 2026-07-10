from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.responses import success_response
from files.serializers import (
    CreateUploadSessionResponseSerializer,
    CreateUploadSessionSerializer,
    FinalizeUploadSerializer,
    FinalizeUploadResponseSerializer,
)
from files.services import FilesService


class CreateUploadSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_serializer = CreateUploadSessionSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)

        result = FilesService.create_upload_session(
            workspace=request_serializer.validated_data["workspace"],
            user=request.user,
            files=request_serializer.validated_data["files"],
        )

        response_serializer = CreateUploadSessionResponseSerializer(
            data=result
        )
        response_serializer.is_valid(raise_exception=True)

        return success_response(
            message="Upload session created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class FinalizeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_serializer = FinalizeUploadSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        result = FilesService.finalize_upload(
            upload_session_id=request_serializer.validated_data["upload_session_id"],
            user=request.user,
        )

        response_serializer = FinalizeUploadResponseSerializer(data=result)
        response_serializer.is_valid(raise_exception=True)

        return success_response(
            message="Upload session finalized successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_200_OK,
        )