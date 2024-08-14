#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

from functools import wraps
from typing import Callable

import redis
import requests

redis_client = redis.Redis()


def cache_with_expiration(method: Callable, expiration: int) -> Callable:
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
        # Track the number of times the URL is accessed
        redis_client.incr(f"count:{url}")

        # Check if the URL is already cached
        cached_result = redis_client.get(url)
        if cached_result:
            return cached_result.decode("utf-8")

        # Call the original method to get the result
        result = method(url)

        # Cache the result with an expiration time
        redis_client.setex(url, expiration, result)

        return result

    return wrapper


@cache_with_expiration(10)
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
