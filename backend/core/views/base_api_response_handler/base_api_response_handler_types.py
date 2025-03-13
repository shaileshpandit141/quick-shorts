from typing import Any, TypedDict

TypeData = dict[str, Any] | list[dict[str, Any]]


TypeErrors = dict[str, Any]


class TypeResponsePayload(TypedDict):
    message: str
    data: TypeData
    errors: TypeErrors


class TypeSuccessPayload(TypedDict):
    message: str
    data: TypeData


class TypeErrorPayload(TypedDict):
    message: str
    errors: TypeErrors
