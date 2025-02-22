from datetime import datetime
from typing import Any, Dict, Optional


# Meta Data Helpers
def get_meta(
    custom_meta: Optional[Dict[str, Any]] = None,
    response_time: str = "N/A",
    request_id: str = "N/A",
) -> Dict[str, Any]:
    meta = {
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat(),
        "response_time": response_time,
        "documentation_url": "N/A",
    }
    if custom_meta:
        meta.update(custom_meta)
    return meta
