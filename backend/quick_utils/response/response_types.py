from typing import (
    TypedDict,
    Literal,
    Dict,
    Any,
    Optional,
    NotRequired,
    Union,
    List
)
from backend.throttling import (
    AnonRateThrottle,
    UserRateThrottle
)


class ThrottleRateLimitType(TypedDict):
    """Type for rate limit information"""
    limit: int
    remaining: int
    reset_time: str


class MetaType(TypedDict):
    """Type for API response metadata"""
    request_id: NotRequired[str]
    timestamp: NotRequired[str]
    documentation_url: NotRequired[str]
    rate_limit: NotRequired[Dict[str, ThrottleRateLimitType]]


class DetailType(TypedDict):
    """Type for error detail information"""
    requirements: NotRequired[List[str]]
    limit: NotRequired[int]
    remaining: NotRequired[int]
    reset_time: NotRequired[int]
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    pattern: NotRequired[str]
    retry_after: NotRequired[str]
    field_type: NotRequired[str]
    expected_format: NotRequired[str]
    example_value: NotRequired[str]


class ErrorsType(TypedDict):
    """Type for API error responses"""
    field: str
    code: str
    message: str
    details: Optional[DetailType | Dict[str, Any]]


class ResponseDataType(TypedDict):
    """Type for main API response structure"""
    status: Literal["succeeded", "failed"]
    message: str
    data: Optional[Dict[str, Any] | List[Dict[str, Any]]]
    errors: Optional[List[ErrorsType]]
    meta: NotRequired[MetaType | None]


# Type alias for throttle classes
ThrottleType = Union[AnonRateThrottle, UserRateThrottle, None]
