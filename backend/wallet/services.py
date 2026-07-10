from django.db import IntegrityError, DatabaseError, transaction
import logging

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

logger = logging.getLogger("django")


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

            logger.info("Created wallet for user ID: %s with initial balance: %s", user.id, INITIAL_USER_TOKEN_BALANCE)
            return wallet

        except IntegrityError:
            logger.warning("Wallet creation failed: Wallet already exists for user ID: %s", user.id)
            raise WalletAlreadyExistsException()

        except DatabaseError as e:
            logger.error("Database error during wallet creation for user ID: %s - %s", user.id, e, exc_info=True)
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
            
            logger.info("Credited %s tokens to wallet ID: %s (Reason: %s). New balance: %s", amount, wallet.id, reason, wallet.token_balance)
            return wallet

        except DatabaseError as e:
            logger.error("Database error crediting tokens for wallet ID: %s - %s", wallet.id, e, exc_info=True)
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
            logger.warning("Debit failed: Insufficient balance for wallet ID: %s. Requested: %s, Available: %s", wallet.id, amount, wallet.token_balance)
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

            logger.info("Debited %s tokens from wallet ID: %s (Reason: %s). New balance: %s", amount, wallet.id, reason, wallet.token_balance)
            return wallet

        except DatabaseError as e:
            logger.error("Database error debiting tokens for wallet ID: %s - %s", wallet.id, e, exc_info=True)
            raise WalletException(
                detail="Failed to debit tokens."
            )