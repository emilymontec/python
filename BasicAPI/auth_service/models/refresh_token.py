from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    token_hash = Column(String, nullable=False)
    revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)