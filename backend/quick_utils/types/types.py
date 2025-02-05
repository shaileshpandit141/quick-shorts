from typing import Any, Dict, List, NotRequired, Optional, TypedDict


class ErrorsFieldType(TypedDict):
    """Type for API error responses"""

    field: str
    code: str
    message: str
    details: Optional[Dict[str, Any]]


ErrorsType = List[ErrorsFieldType]


class ResponseDataType(TypedDict):
    """Type for main API response structure"""

    message: str
    data: NotRequired[Dict[str, Any] | List[Dict[str, Any]]]
    errors: NotRequired[ErrorsType]


class ThrottleRateLimitType(TypedDict):
    """Type for rate limit information"""

    type: str
    limit: int
    remaining: int
    reset_time: str
    retry_after: str
