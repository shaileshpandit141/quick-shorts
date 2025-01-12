from rest_framework.throttling import (
    UserRateThrottle as DRFUserRateThrottle
)
from quick_utils.as_api_response_format import as_api_response_format

class UserRateThrottle(DRFUserRateThrottle):
    def throttle_error_message(self):
        rate_limit = self.get_rate()
        wait_time = self.wait()
        if wait_time is not None:
            retry_after = str(int(wait_time))
        else:
            retry_after = "0"

        return as_api_response_format({
            "status": "failed",
            "message": "Sorry, you have made too many requests.",
            "data": None,
            "errors": [{
                "field": "request",
                "code": "rate_limit_exceeded",
                "message": "API rate limit has been reached. Please slow down your request rate.",
                "details": {
                    "limit": rate_limit,
                    "reset_time": int(self.timer()),
                    "retry_after": retry_after
                }
            }]
        })
