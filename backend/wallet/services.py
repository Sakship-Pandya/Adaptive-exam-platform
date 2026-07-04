from django.db import IntegrityError, DatabaseError, transaction

from common.constants import INITIAL_USER_TOKEN_BALANCE

from .exceptions import (
    InsufficientTokenBalanceException,
    WalletAlreadyExistsException,
    WalletException,
)
from common.choices import TransactionReason, TransactionType
from .models import (
    TokenTransaction,
    UserWallet,
)


class WalletService:
    @staticmethod
    @transaction.atomic
    def create_wallet(user):
        try:
            wallet = UserWallet.objects.create(
                user=user,
                token_balance=INITIAL_USER_TOKEN_BALANCE,
                total_tokens_earned=INITIAL_USER_TOKEN_BALANCE,
                total_tokens_spent=0,
            )

            TokenTransaction.objects.create(
                wallet=wallet,
                transaction_type=TransactionType.CREDIT,
                reason=TransactionReason.INITIAL_ALLOCATION,
                amount=INITIAL_USER_TOKEN_BALANCE,
                balance_after_transaction=INITIAL_USER_TOKEN_BALANCE,
                description="Initial token allocation during account registration.",
            )

            return wallet

        except IntegrityError:
            raise WalletAlreadyExistsException()

        except DatabaseError:
            raise WalletException(
                detail="Failed to create user wallet."
            )

    @staticmethod
    @transaction.atomic
    def credit_tokens(
        wallet,
        amount,
        reason,
        description="",
    ):
        try:
            wallet.token_balance += amount
            wallet.total_tokens_earned += amount

            wallet.save(
                update_fields=[
                    "token_balance",
                    "total_tokens_earned",
                    "updated_at",
                ]
            )

            TokenTransaction.objects.create(
                wallet=wallet,
                transaction_type=TransactionType.CREDIT,
                reason=reason,
                amount=amount,
                balance_after_transaction=wallet.token_balance,
                description=description,
            )

            return wallet

        except DatabaseError:
            raise WalletException(
                detail="Failed to credit tokens."
            )

    @staticmethod
    @transaction.atomic
    def debit_tokens(
        wallet,
        amount,
        reason,
        description="",
    ):
        if wallet.token_balance < amount:
            raise InsufficientTokenBalanceException()

        try:
            wallet.token_balance -= amount
            wallet.total_tokens_spent += amount

            wallet.save(
                update_fields=[
                    "token_balance",
                    "total_tokens_spent",
                    "updated_at",
                ]
            )

            TokenTransaction.objects.create(
                wallet=wallet,
                transaction_type=TransactionType.DEBIT,
                reason=reason,
                amount=amount,
                balance_after_transaction=wallet.token_balance,
                description=description,
            )

            return wallet

        except DatabaseError:
            raise WalletException(
                detail="Failed to debit tokens."
            )