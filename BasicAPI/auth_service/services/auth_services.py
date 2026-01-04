from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from repositories import user_repository, token_repository
from utils.security import verify_password, hash_password
from utils.jwt import create_token
from models.user import User, Role
from core.config import settings


def register(db: Session, email: str, password: str, role: Role = None):
    # Si no se especifica rol, usar lógica por defecto
    if role is None:
        user_count = user_repository.count_all(db)
        role = Role.admin if user_count == 0 else Role.user
    
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    return user_repository.create(db, user)


def login(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)

    if not user:
        return None

    # Verificar contraseña
    if not verify_password(password, user.password_hash):
        return None

    access_token = create_token(
        {
            "sub": str(user.id),
            "role": user.role.value
        },
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_token(
        {
            "sub": str(user.id)
        },
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # 🔐 Rotación de refresh tokens
    token_repository.revoke_tokens(db, user.id)

    token_repository.store_token(
        db=db,
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow()
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return access_token, refresh_token
