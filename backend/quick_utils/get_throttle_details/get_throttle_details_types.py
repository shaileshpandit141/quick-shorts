from typing import TypedDict


class ThrottleRateLimitType(TypedDict):
    """Type for rate limit information"""
    limit: int
    remaining: int
    reset_time: str
