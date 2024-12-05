from typing import Any, Dict
from urllib.parse import urlencode

def add_query_params(url: str, params: Dict[str, Any]):
    """
    Adds query parameters to a given URL.

    Args:
        url (str): The base URL to which query parameters should be added.
        params (dict): A dictionary containing query parameters and their values.

    Returns:
        str: The updated URL with the query parameters.
    """
    if not params:
        return url

    query_string = urlencode(params)
    if '?' in url:
        return f"{url}&{query_string}"
    else:
        return f"{url}?{query_string}"
