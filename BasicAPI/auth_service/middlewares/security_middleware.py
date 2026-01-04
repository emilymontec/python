from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from utils.security import validate_jwt, validate_headers, validate_fingerprint

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        validate_headers(request)
        validate_jwt(request)
        validate_fingerprint(request)
        response = await call_next(request)
        return response
