from rest_framework import serializers

from common.choices import FileRole, UploadSessionStatus
from workspace.models import Workspace


class UploadFileSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=FileRole.choices)
    size = serializers.IntegerField(min_value=1)
    content_type = serializers.CharField(max_length=100)

    def validate_filename(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Filename cannot be empty.")

        return value


class CreateUploadSessionSerializer(serializers.Serializer):
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        source="workspace",
    )
    files = UploadFileSerializer(many=True)

    def validate_files(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one file must be provided."
            )

        filenames = set()

        for file in value:
            filename = file["filename"].lower()

            if filename in filenames:
                raise serializers.ValidationError(
                    f"Duplicate filename '{file['filename']}' detected."
                )

            filenames.add(filename)

        return value


class UploadInstructionSerializer(serializers.Serializer):
    upload_session_file_id = serializers.UUIDField()
    original_filename = serializers.CharField()
    role = serializers.ChoiceField(choices=FileRole.choices)
    storage_key = serializers.CharField()
    content_type = serializers.CharField()
    expected_file_size = serializers.IntegerField()
    upload_url = serializers.URLField()


class CreateUploadSessionResponseSerializer(serializers.Serializer):
    upload_session_id = serializers.UUIDField()
    expires_at = serializers.DateTimeField()
    files = UploadInstructionSerializer(many=True)


class FinalizeUploadSerializer(serializers.Serializer):
    upload_session_id = serializers.UUIDField()


class FinalizeUploadResponseSerializer(serializers.Serializer):
    upload_session_id = serializers.UUIDField()
    status = serializers.ChoiceField(
        choices=UploadSessionStatus.choices
    )
    verified_file_count = serializers.IntegerField(min_value=0)
    completed_at = serializers.DateTimeField()