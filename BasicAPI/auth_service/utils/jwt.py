from datetime import datetime, timedelta
import jwt
from core.config import settings




def create_token(data: dict, expires_delta: timedelta):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")




def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise
    except jwt.JWTError:
        raise