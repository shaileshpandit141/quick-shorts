from typing import Any, TypedDict, NotRequired

TypeData = dict[str, Any] | list[dict[str, Any]]


class TypeDefaultErrorFields(TypedDict):
    detail: NotRequired[str]
    non_field_errors: NotRequired[list[str]]


TypeModelErrorFields = dict[str, list[str]]


TypeErrors = TypeModelErrorFields | TypeDefaultErrorFields


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
