from typing import TypedDict


class ThrottleRateLimitType(TypedDict):
    """Type for rate limit information"""

    type: str
    limit: int
    remaining: int
    reset_time: str
    retry_after: str
