from rest_framework.throttling import SimpleRateThrottle
from django.conf import settings

class AuthRateThrottle(SimpleRateThrottle):
    scope = 'custom'

    def get_cache_key(self, request, view):
        """
        Generate a cache key unique to each device on the same network.
        Use a combination of router IP and a device-specific identifier.
        """
        router_ip = self.get_ident(request)  # Identifies the network's public IP
        # Use user ID for authenticated users, or fall back to user-agent for anonymous users
        if request.user.is_authenticated:
            device_id = f"user_{request.user.id}"
        else:
            device_id = request.headers.get("User-Agent", "unknown_device")

        return f"throttle_{router_ip}_{device_id}_{view.__class__.__name__}"

    def get_rate(self):
        """
        Define a custom rate for throttling.
        """
        default_rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        return default_rates.get("auth", "30/minute")  # Default rate

    def allow_request(self, request, view):
        """
        Apply the rate and determine if the request is allowed.
        """
        self.request = request  # Store request for get_rate
        self.rate = self.get_rate()
        return super().allow_request(request, view)
