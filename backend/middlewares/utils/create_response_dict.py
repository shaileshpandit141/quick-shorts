from .get_meta import get_meta
from .types import DataType


def create_response_dict(
    success: bool,
    validate_data: DataType,
    throttles: list,
    response_time: str,
    request_id: str,
    status_code: int = 200,
) -> dict:
    return {
        "status": "succeeded" if success else "failed",
        "status_code": status_code,
        "message": validate_data["message"],
        "data": validate_data.get("data") if success else None,
        "errors": validate_data.get("errors", []) if not success else [],
        "meta": get_meta({"rate_limits": throttles}, response_time, request_id),
    }
