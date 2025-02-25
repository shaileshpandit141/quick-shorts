from typing import Any, Dict, List, NotRequired, TypedDict


# Type Definitions
class DataType(TypedDict):
    message: str
    data: NotRequired[Dict[str, Any]]
    errors: NotRequired[List[Dict[str, Any]]]
