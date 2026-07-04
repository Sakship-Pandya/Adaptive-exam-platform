from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from common.models import BaseModel
from common.choices import AccountStatus

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model for authentication.
    Username is used as the login identifier.
    """

    email = models.EmailField(unique=True, max_length=255, db_index=True)

    username = models.CharField(max_length=50, unique=True, db_index=True)

    account_status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)

    is_active = models.BooleanField(default=True, help_text="Designates whether this account can authenticate.")

    is_staff = models.BooleanField(default=False, help_text="Allows access to the Django admin site.")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        # Creating index for the database tables for faster searching
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
            models.Index(fields=["account_status"]),
        ]

    def __str__(self):
        return self.email