#!/usr/bin/env python3
import redis
import requests
from typing import Callable
from functools import wraps

# Redis client setup
_redis = redis.Redis()

def cache_with_count(expire: int = 10):
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str):
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            _redis.incr(count_key)
            cached = _redis.get(cache_key)
            if cached:
                return cached.decode('utf-8')
            result = method(url)
            _redis.setex(cache_key, expire, result)
            return result
        return wrapper
    return decorator

@cache_with_count(expire=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
