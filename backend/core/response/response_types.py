from typing import Any, NotRequired, TypedDict

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
