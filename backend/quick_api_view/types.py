from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle
)
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


class PaginationType(TypedDict):
    """Type for pagination information"""
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int
    has_next: bool
    has_previous: bool


class RateLimitType(TypedDict):
    """Type for rate limit information"""
    limit: int
    remaining: int
    reset_time: str


class MetaType(TypedDict):
    """Type for API response metadata"""
    request_id: str
    timestamp: str
    response_time: str
    documentation_url: str
    rate_limit: NotRequired[RateLimitType]


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
    details: Optional[DetailType]


class DataType(TypedDict):
    """Type for main API response structure"""
    status: Literal["succeeded", "failed"]
    message: str
    data: Optional[Dict[str, Any] | List[Dict[str, Any]]]
    pagination: NotRequired[PaginationType]
    errors: Optional[List[ErrorsType]]
    meta: NotRequired[MetaType]


# Type alias for throttle classes
ThrottleType = Union[AnonRateThrottle, UserRateThrottle, None]
