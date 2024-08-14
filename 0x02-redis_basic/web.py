#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

from functools import wraps
from typing import Callable

import redis
import requests

redis_client = redis.Redis()


def cache_with_expiration(method: Callable) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration (int): The expiration time in seconds.

    Returns:
        Callable: The wrapped function with caching.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function to handle caching and expiration.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL, either from cache or fetched.
        """
        redis_client.incr(f"count:{url}")
        result = redis_client.get(f"result:{url}")

        if result:
            return result.decode("utf-8")

        result = method(url)
        redis_client.set(f"count:{url}", 0)
        redis_client.setex(f"result:{url}", 10, result)

        return result

    return wrapper


@cache_with_expiration
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
