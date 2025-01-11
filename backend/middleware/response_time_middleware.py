import time

class ResponseTimeMiddleware:
    """
    Middleware that measures response time and adds it as a header.

    Adds X-Response-Time header to responses containing the time taken
    to process the request in seconds.
    """

    def __init__(self, get_response):
        """Store the get_response callable for processing."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request, measure time taken, and add timing header.

        Args:
            request: The HTTP request object

        Returns:
            Response object with X-Response-Time header added
        """
        # Start timing
        start_time = time.perf_counter()

        # Process the request
        response = self.get_response(request)

        # Calculate duration and add header
        duration = time.perf_counter() - start_time
        response["X-Response-Time"] = f"{duration:.5f} seconds"

        return response
