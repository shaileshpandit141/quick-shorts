from rest_framework.throttling import AnonRateThrottle as DRFAnonRateThrottle

class AnonRateThrottle(DRFAnonRateThrottle):
    def throttle_error_message(self):
        return {
            "status": "error",
            "message": "Sorry, you have made too many requests.",
            "errors": {
                'non_filed_errors': [
                    "API rate limit has been reached. Please slow down your request rate."
                ]
            }
        }
