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
        """
        Callable: The wrapped method with call counting.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def replay(fn: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method to replay the history for.
    """
    redis_instance = fn.__self__._redis
    fn_name = fn.__qualname__
    input_key = f"{fn_name}:inputs"
    output_key = f"{fn_name}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{fn_name} was called {len(inputs)} times:")
    for input_val, output_val in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                fn_name,
                input_val.decode("utf-8"),
                output_val,
            )
        )


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with input/output history tracking.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store the history of inputs and outputs.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            The result of the original method call.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

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
    @call_history
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
