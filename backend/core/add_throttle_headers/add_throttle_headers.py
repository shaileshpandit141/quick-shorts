from logging import getLogger
from typing import Any, Dict, List, Optional
from rest_framework.response import Response

logger = getLogger(__name__)


def add_throttle_headers(
    response: Response, throttle_limits: Optional[List[Dict[str, Any]] | Any]
) -> Any:
    """Adds standardized rate limit headers to the response.

    Args:
        response (Response): The DRF response object to update.
        throttle_limits (Optional[List[Dict[str, Any]]]): A list of throttle details.
    """
    if not throttle_limits:
        return

    throttle_headers = {}

    try:
        required_keys = {"type", "limit", "remaining", "reset_time", "retry_after"}

        for throttle in throttle_limits:
            if not required_keys.issubset(throttle):
                continue

            throttle_type = throttle["type"]
            throttle_headers.update(
                {
                    f"X-RateLimit-{throttle_type}-Limit": str(throttle["limit"]),
                    f"X-RateLimit-{throttle_type}-Remaining": str(
                        throttle["remaining"]
                    ),
                    f"X-RateLimit-{throttle_type}-Reset": str(throttle["reset_time"]),
                    f"X-RateLimit-{throttle_type}-Retry-After": str(
                        throttle["retry_after"]
                    ),
                }
            )

        if throttle_headers:
            setattr(response, "headers", {**response.headers, **throttle_headers})
            logger.debug(f"Added throttle headers: {throttle_headers}")
    except Exception as e:
        logger.error(f"Error adding throttle details: {e}", exc_info=True)
