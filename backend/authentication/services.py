from django.contrib.auth import get_user_model
from django.db import IntegrityError, DatabaseError, transaction
from wallet.services import WalletService

from .exceptions import UserRegistrationException

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
