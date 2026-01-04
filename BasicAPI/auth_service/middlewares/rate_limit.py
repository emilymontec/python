from fastapi import Request, HTTPException
from datetime import datetime
from typing import Callable

# In-memory rate limiting
rate_limits = {}

def rate_limit(endpoint: str, limit: int, window: int):
    def decorator(func: Callable):
        async def wrapper(request: Request, *args, **kwargs):
            user_id = request.state.user_id
            if not user_id:
                raise HTTPException(status_code=403, detail="User ID not found.")
            key = f"{user_id}_{endpoint}"
            timestamps = rate_limits.get(key, [])
            now = datetime.now().timestamp()
            timestamps = [t for t in timestamps if now - t < window]
            if len(timestamps) >= limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded.")
            timestamps.append(now)
            rate_limits[key] = timestamps
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
