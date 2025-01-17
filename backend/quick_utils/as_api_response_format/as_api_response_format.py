from datetime import datetime
import uuid
from ..types import ResponseDataType

def as_api_response_format(data: ResponseDataType) -> ResponseDataType:
    errors = data.get("errors", None)

    payload: ResponseDataType = {
        "status": data["status"],
        "message": data["message"],
        "data": data.get("data", None),
        "errors": [] if errors is None else errors,
        "meta": None
    }

    meta = data.get("meta", None)
    if meta is None:
        payload["meta"] = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "documentation_url": "https://api.example.com/docs"
        }
    else:
        payload["meta"] = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "documentation_url": "https://api.example.com/docs",
            **meta
        }

    return payload
