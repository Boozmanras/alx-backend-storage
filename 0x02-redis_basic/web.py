#!/usr/bin/env python3
"""
Module for implementing a web cache and tracker using Redis
"""
import redis
import requests
from typing import Callable
from functools import wraps


def cache_and_track_url(method: Callable) -> Callable:
    """
    Decorator to cache the page content and track URL access count
    Args:
        method: The method to be decorate
    Returns:
        Callable: The wrapped function
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that implements caching and tracking
        """
        redis_client = redis.Redis()

        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        redis_client.incr(count_key)

        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        content = method(url)
        redis_client.setex(cache_key, 10, content)

        return content

    return wrapper


@cache_and_track_url
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a URL and cache it
    Args:
        url: The URL to fetch
    Returns:
        str: The HTML content of the page
    """
    response = requests.get(url)
    return response.text
