from urllib.parse import urlparse


def is_valid_url(url) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)
