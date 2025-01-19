from typing import TypedDict


class TokenGeneratorResponse(TypedDict):
    """Response object containing token details and message.

    Attributes:
        token: Generated auth token string
        token_salt: Salt value used in token generation 
        message: Status or success message
    """
    token: str
    token_salt: str
    message: str
