#!/usr/bin/env python3
import redis
import requests
from typing import Callable
from functools import wraps

# Redis client setup
_redis = redis.Redis()

def get_page(url: str) -> str:
    """Fetch HTML content of a URL and cache the result for 10 seconds."""
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"

    # Increment the access count
    _redis.incr(count_key)

    # Check if cached version exists
    cached = _redis.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    # If not cached, fetch and store with expiration
    response = requests.get(url)
    html = response.text
    _redis.setex(cache_key, 10, html)

    return html
