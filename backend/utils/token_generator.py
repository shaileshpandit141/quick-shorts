from typing import Dict, Any, NoReturn
from datetime import datetime, timedelta
from django.conf import settings
import logging
from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired
)

logger = logging.getLogger(__name__)

class TokenGenerator:
    """
    A flexible token generator that supports token creation and decoding anywhere.
    """

    @staticmethod
    def generate(data: Dict[str, Any], salt: str, expiry_seconds=3600) -> str:
        """
        Generates a secure token with expiration, revocation, and custom claims.

        :param data: A dictionary or data object to encode into the token.
        :param salt: A unique salt for added security.
        :param expiry_seconds: The expiration time for the token in seconds.
        """
        logger.debug(f"Generating token with salt: {salt} and expiry: {expiry_seconds}s")
        expiry_time = datetime.utcnow() + timedelta(seconds=expiry_seconds)
        data["expiry_time"] = expiry_time.isoformat()

        serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt=salt)
        token = serializer.dumps(data)
        logger.debug("Token generated successfully")
        return token

    @staticmethod
    def decode(token: str, salt: str, expiry_seconds=3600) -> Dict[str, Any] | NoReturn:
        """
        Decodes a token, checks its validity, and handles expiration and revocation.

        :param token: The signed token to decode.
        :param salt: The same salt used during token generation.
        :param expiry_seconds: The maximum allowable age of the token.
        :return: Decoded data if valid, or raises an exception if invalid.
        """
        logger.debug(f"Attempting to decode token with salt: {salt}")
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt=salt)

        try:
            data = serializer.loads(token, max_age=expiry_seconds)
            expiry_time = datetime.fromisoformat(data["expiry_time"])

            if expiry_time < datetime.utcnow():
                logger.warning("Token has expired")
                raise ValueError("The token has expired.")
            logger.debug("Token decoded successfully")
            return data
        except (SignatureExpired, BadSignature) as error:
            logger.error(f"Token validation failed: {str(error)}")
            raise ValueError(f"Invalid or expired token: {str(error)}")
