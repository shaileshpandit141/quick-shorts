from rest_framework.throttling import (
    UserRateThrottle as DRFUserRateThrottle
)

class UserRateThrottle(DRFUserRateThrottle):
    def throttle_error_message(self):
        rate_limit = self.get_rate()
        wait_time = self.wait()
        if wait_time is not None:
            retry_after = str(int(wait_time))
        else:
            retry_after = "0"

        return [{
            "field": "request",
            "code": "rate_limit_exceeded",
            "message": "API rate limit has been reached. Please slow down your request rate.",
            "details": {
                "limit": rate_limit,
                "reset_time": int(self.timer()),
                "retry_after": retry_after
            }
        }]
