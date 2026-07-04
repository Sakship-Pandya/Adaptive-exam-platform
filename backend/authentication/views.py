from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from common.responses import success_response

from .exceptions import AuthenticationException
from .serializers import RegisterSerializer
from .services import AuthenticationService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = AuthenticationService.register_user(serializer.validated_data)

        except AuthenticationException as exc:
            raise exc

        return success_response(
            message="User registered successfully.",
            data={
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            status_code=status.HTTP_201_CREATED,
        )