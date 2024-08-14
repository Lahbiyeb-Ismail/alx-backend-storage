#!/usr/bin/env python3

"""
Cache class using redis
"""

import uuid
from typing import Union

import redis


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method that takes a data argument and returns a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
