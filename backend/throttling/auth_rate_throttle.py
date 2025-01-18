from rest_framework.throttling import SimpleRateThrottle
from django.conf import settings

class AuthRateThrottle(SimpleRateThrottle):
    scope = 'custom'

    def get_cache_key(self, request, view):
        """
        Generate a unique cache key based on the user type.
        """
        if request.user.is_authenticated:
            # Use the user ID for authenticated users
            return f"throttle_user_{request.user.id}"
        else:
            # Use the IP address for anonymous users
            return self.get_ident(request)

    def get_rate(self):
        """
        Define custom rates by checking request user in instance variable.
        """
        default_rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        return default_rates.get("auth", "30/minute")

    def allow_request(self, request, view):
        """
        Apply the rate and call the parent method to determine if the request is allowed.
        """
        self.request = request  # Store request for get_rate
        self.rate = self.get_rate()
        return super().allow_request(request, view)
