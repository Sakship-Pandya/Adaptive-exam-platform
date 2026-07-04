from rest_framework import status
from rest_framework.exceptions import APIException


class WalletException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "wallet_error"
    default_detail = "A wallet operation failed."


class WalletAlreadyExistsException(WalletException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "wallet_already_exists"
    default_detail = "A wallet already exists for this user."


class WalletNotFoundException(WalletException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "wallet_not_found"
    default_detail = "The requested wallet could not be found."


class InsufficientTokenBalanceException(WalletException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "insufficient_token_balance"
    default_detail = "Insufficient token balance to complete this operation."