from typing import (
    TypedDict,
    Literal,
    Dict,
    Any,
    Optional,
    NotRequired,
    List
)


class MetaType(TypedDict):
    """Type for API response metadata"""
    request_id: str
    timestamp: str
    documentation_url: str


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
