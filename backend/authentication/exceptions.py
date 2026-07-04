from rest_framework.exceptions import APIException
from rest_framework import status


class AuthenticationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "authentication_error"
    default_detail = "Authentication operation failed."


class UserRegistrationException(AuthenticationException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "user_registration_failed"
    default_detail = "Unable to register user."


class InvalidCredentialsException(AuthenticationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "invalid_credentials"
    default_detail = "Invalid username or password."


class InactiveAccountException(AuthenticationException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "inactive_account"
    default_detail = "Your account is inactive."


class InvalidTokenException(AuthenticationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "invalid_token"
    default_detail = "The provided token is invalid."


class TokenBlacklistException(AuthenticationException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "token_blacklist_failed"
    default_detail = "Unable to blacklist the provided token."