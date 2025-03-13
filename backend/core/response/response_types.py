from typing import Any, TypedDict

TypeData = dict[str, Any] | list[dict[str, Any]]


TypeErrors = dict[str, Any]


class TypeResponsePayload(TypedDict):
    message: str
    data: TypeData
    errors: TypeErrors
