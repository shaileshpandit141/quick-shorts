from typing import Any, Dict, List, NotRequired, TypedDict


class TypeError(TypedDict):
    field: str
    code: str
    message: str
    details: NotRequired[Dict[str, Any]]


TypeErrors = List[TypeError]
