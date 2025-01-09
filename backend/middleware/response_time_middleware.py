import time

class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()  # Record the start time
        response = self.get_response(request)  # Process the request
        duration = time.perf_counter() - start_time  # Calculate response time
        response["X-Response-Time"] = f"{duration:.3f} seconds"  # Add it to headers
        request.response_time = f"{duration:.3f} seconds"  # Attach to request object
        return response
