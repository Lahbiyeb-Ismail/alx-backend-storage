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
        key = "cached:" + url
        cached_value = redis_client.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        redis_client.incr(key_count)
        redis_client.set(key, html_content, ex=10)
        redis_client.expire(key, 10)
        return html_content

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


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
