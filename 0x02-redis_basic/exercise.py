#!/usr/bin/env python3
"""
Redis Cache module for storing and retrieving data
with decorators for tracking calls
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called
    Args:
        method: The method to be decorated
    Returns:
        Callable: The wrapped function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count and calls the method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function
    Args:
        method: The method to be decorated
    Returns:
        Callable: The wrapped function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores inputs and outputs in Redis lists
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    Args:
        method: The method whose history to display
    """
    redis_instance = redis.Redis()
    method_name = method.__qualname__
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)
    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(
            f"{method_name}(*{input_args.decode('utf-8')}) -> "
            f"{output.decode('utf-8')}"
        )


class Cache:
    """
    Cache class for storing data in Redis
    """
    def __init__(self) -> None:
        """
        Initialize the Cache instance with a Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a random key
        Args:
            data: Data to store (can be str, bytes, int, or float)
        Returns:
            str: The key under which the data was stored
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and convert it to the desired format
        Args:
            key: Key to retrieve data for
            fn: Optional function to convert the data
        Returns:
            The data in its original format, or None if the key doesn't exist
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis
        Args:
            key: Key to retrieve data for
        Returns:
            Optional[str]: The string value, or None if the key doesn't exist
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis
        Args:
            key: Key to retrieve data for
        Returns:
            Optional[int]: The integer value, or None if the key doesn't exist
        """
        return self.get(key, int)
