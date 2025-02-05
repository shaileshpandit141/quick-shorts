def get_client_ip(request) -> str:
    """
    Get the client's IP address from the request.

    Attempts to get the real IP address from X-Forwarded-For header first,
    falling back to REMOTE_ADDR if not found.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Return first IP in case of multiple addresses in X-Forwarded-For
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")
