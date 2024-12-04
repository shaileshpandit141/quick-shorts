from rest_framework.throttling import UserRateThrottle as DRFUserRateThrottle

class UserRateThrottle(DRFUserRateThrottle):
    def throttle_error_message(self):
        return {
            "status": "error",
            "message": "Too many requests. Please try again later.",
            "errors": {
                'non_filed_errors': [
                    "You have reached your rate limit. Please wait before making more requests."
                ]
            }
        }
