from fastapi import HTTPException, Request
from time import time
from functools import wraps

RATE_LIMITS = {}

def rate_limit(key: str, limit: int, window: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            timestamps = RATE_LIMITS.get(key, [])
            timestamps = [t for t in timestamps if now - t < window]

            if len(timestamps) >= limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            timestamps.append(now)
            RATE_LIMITS[key] = timestamps
            return func(*args, **kwargs)
        return wrapper
    return decorator
