import logging
import time
from typing import Any

from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ResponseTimeMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        start_time = time.perf_counter()
        response = self.get_response(request)
        end_time = time.perf_counter()

        response_time = f"{round(end_time - start_time, 6)} seconds"
        response["X-Response-Time"] = response_time

        logger.info(f"Request processed in {response_time}")

        if isinstance(response, Response) and isinstance(response.data, dict):
            try:
                response.data.setdefault("meta", {})["response_time"] = response_time
            except Exception as error:
                logger.error(f"Error adding response time to meta: {error}")

            # Force re-rendering of response
            setattr(response, "_is_rendered", False)
            response.render()

        return response
