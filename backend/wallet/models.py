from django.conf import settings
from django.db import models

from common.choices import TransactionReason, TransactionType
from common.models import BaseModel


class UserWallet(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )

    token_balance = models.PositiveIntegerField(
        default=0,
    )

    total_tokens_earned = models.PositiveBigIntegerField(
        default=0,
    )

    total_tokens_spent = models.PositiveBigIntegerField(
        default=0,
    )

    class Meta:
        db_table = "user_wallets"
        verbose_name = "User Wallet"
        verbose_name_plural = "User Wallets"
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class TokenTransaction(BaseModel):
    wallet = models.ForeignKey(
        UserWallet,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    reason = models.CharField(
        max_length=50,
        choices=TransactionReason.choices,
    )

    amount = models.PositiveIntegerField()

    balance_after_transaction = models.PositiveIntegerField()

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "token_transactions"
        verbose_name = "Token Transaction"
        verbose_name_plural = "Token Transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["wallet"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return (
            f"{self.transaction_type} | "
            f"{self.amount} Tokens | "
            f"{self.wallet.user.username}"
        )