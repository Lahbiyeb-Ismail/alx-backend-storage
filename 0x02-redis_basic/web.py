#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

from functools import wraps
from typing import Callable

import redis
import requests

redis_client = redis.Redis()


def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration (int): The expiration time in seconds.

    Returns:
        Callable: The wrapped function with caching.
    """

    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            redis_client.incr(f"count:{url}")

            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode("utf-8")

            result = method(url)

            redis_client.setex(url, expiration, result)

            return result

        return wrapper

    return decorator


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
