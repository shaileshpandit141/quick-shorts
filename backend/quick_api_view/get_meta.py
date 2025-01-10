from datetime import datetime
import pytz
import uuid
from .types import ThrottleType, MetaType

def get_meta(request, throttle: ThrottleType=None, history=None) -> MetaType:
    """
    Generates request metadata with optional rate limiting information.

    Args:
        request: HTTP request object
        throttle: Optional rate limiting throttle instance
        history: Optional list of timestamps from previous requests

    Returns:
        MetaType: Dict containing request metadata and rate limit info if throttle provided
    """

    meta_data: MetaType = {
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "response_time": getattr(request, "response_time", "N/A"),
        "documentation_url": "https://api.example.com/docs",
    }

    if throttle is not None:
        if history is None:
            history = throttle.history or []

        # Get throttle settings
        limit = throttle.num_requests or 0  # Maximum requests per window
        duration = throttle.duration         # Time window in seconds

        # Calculate remaining requests
        remaining = max(0, limit - len(history))

        # Get reset time based on first request in history
        if history:
            reset_time = history[0] + duration
        else:
            reset_time = datetime.now(pytz.UTC)

        return {
            **meta_data,
            "rate_limit": {
                "limit": limit,
                "remaining": remaining,
                "reset_time": reset_time.isoformat(),
            }
        }

    return meta_data
