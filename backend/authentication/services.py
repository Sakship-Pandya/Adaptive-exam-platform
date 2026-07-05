from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError, DatabaseError, transaction
from wallet.services import WalletService
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import UserRegistrationException, InvalidCredentialsException, InactiveAccountException

User = get_user_model()


class AuthenticationService:
    @staticmethod
    @transaction.atomic
    def register_user(validated_data):
        data = validated_data.copy()
        data.pop("confirm_password")
        try:
            user = User.objects.create_user(**data)
            WalletService.create_wallet(user)
            return user
        except IntegrityError:
            raise UserRegistrationException(
                detail="A user with the provided username or email already exists."
            )
        except DatabaseError:
            raise UserRegistrationException(
                detail="Failed to create user."
            )
    @staticmethod
    def authenticate_user(validated_data):
        username = validated_data["username"]
        password = validated_data["password"]

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveAccountException()

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }