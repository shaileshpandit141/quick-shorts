from typing import Dict, Any, NoReturn
from datetime import datetime, timedelta  # type: ignore
from django.conf import settings
import logging
from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired
)
import secrets
from .token_generator_types import TokenGeneratorResponse

logger = logging.getLogger(__name__)


class TokenGenerator:
    """
    A flexible token generator that supports token creation and decoding anywhere.
    """

    @staticmethod
    def generate_one_time_token(num_bytes:int = 16):
        return secrets.token_hex(num_bytes)

    @staticmethod
    def generate(payload: Dict[str, Any], token_expiry_seconds=3600) -> TokenGeneratorResponse:
        """
        Generates a secure token with expiration, revocation, and custom claims.

        :param payload: A dictionary or data object to encode into the token.
        :param salt: A unique salt for added security.
        :param token_expiry_seconds: The expiration time for the token in seconds.
        """
        token_expiry_time = datetime.utcnow() + timedelta(seconds=token_expiry_seconds)
        payload["expiry_time"] = token_expiry_time.isoformat()

        token_salt = TokenGenerator.generate_one_time_token()
        logger.debug(f"Generating token with salt: {token_salt} and expiry: {token_expiry_seconds}s")

        token_serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt=token_salt)
        generated_token = token_serializer.dumps(payload)
        logger.debug("Token generated successfully")
        return {
            'token': generated_token,
            'token_salt': token_salt,
            'message': 'Token generated successfully'
        }

    @staticmethod
    def decode(encoded_token: str, token_salt: str, token_expiry_seconds=3600) -> Dict[str, Any] | NoReturn:
        """
        Decodes a token, checks its validity, and handles expiration and revocation.

        :param encoded_token: The signed token to decode.
        :param token_salt: The same salt used during token generation.
        :param token_expiry_seconds: The maximum allowable age of the token.
        :return: Decoded data if valid, or raises an exception if invalid.
        """
        logger.debug(f"Attempting to decode token with salt: {token_salt}")
        token_serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt=token_salt)

        try:
            decoded_payload = token_serializer.loads(encoded_token, max_age=token_expiry_seconds)
            token_expiry_time = datetime.fromisoformat(decoded_payload["expiry_time"])

            if token_expiry_time < datetime.utcnow():
                logger.warning("Token has expired")
                raise ValueError("The token has expired. Please request a new token.")
            logger.debug("Token decoded successfully")
            decoded_payload['message'] = 'Token decoded successfully'
            return decoded_payload
        except (SignatureExpired, BadSignature) as validation_error:
            logger.error(f"Token validation failed: {str(validation_error)}")
            raise ValueError("Invalid or expired token. Please request a new token.")
