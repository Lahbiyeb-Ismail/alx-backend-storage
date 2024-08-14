#!/usr/bin/env python3

"""
Cache class to interact with a Redis database.
"""

import uuid
from functools import wraps
from typing import Callable, Optional, Union

import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count for the method
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        # Call the original method
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class to interact with a Redis database.

    Attributes:
        _redis (redis.Redis): Instance of the Redis client.
    """

    def __init__(self):
        """
        Initialize the Cache instance and flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key and optionally
        apply a conversion function.

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]): A callable to convert
            the data to the desired format.

        Returns:
            Union[str, bytes, int, float, None]:
            The retrieved data, optionally converted.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis by key and convert it to a string.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The retrieved data as a string,
            or None if the key does not exist.
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis by key and convert it to an integer.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, int)
