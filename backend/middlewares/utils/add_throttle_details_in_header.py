from logging import getLogger
from typing import Any, Dict, List

from .add_response_headers import add_response_headers

# Configure logger
logger = getLogger(__name__)


def add_throttle_details_in_header(
    response: Any, throttles: List[Dict[str, Any]]
) -> None:
    if not throttles:
        return

    try:
        headers = {}
        for throttle in throttles:
            if not all(
                key in throttle
                for key in [
                    "type",
                    "limit",
                    "remaining",
                    "reset_time",
                    "retry_after",
                ]
            ):
                continue

            headers.update(
                {
                    f"X-RateLimit-{throttle['type']}-Limit": str(throttle["limit"]),
                    f"X-RateLimit-{throttle['type']}-Remaining": str(
                        throttle["remaining"]
                    ),
                    f"X-RateLimit-{throttle['type']}-Reset": str(
                        throttle["reset_time"]
                    ),
                    f"X-RateLimit-{throttle['type']}-Retry-After": str(
                        throttle["retry_after"]
                    ),
                }
            )

        if headers:
            add_response_headers(response, headers)
            logger.debug(f"Added throttle headers: {headers}")
    except Exception as e:
        logger.error(f"Error adding throttle details: {str(e)}")
