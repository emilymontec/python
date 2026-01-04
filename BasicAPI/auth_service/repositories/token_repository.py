from sqlalchemy.orm import Session
from models.refresh_token import RefreshToken
from datetime import datetime
import hashlib




def store_token(db: Session, user_id: int, token: str, expires_at: datetime):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    db.add(RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
    db.commit()




def revoke_tokens(db: Session, user_id: int):
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({"revoked": True})
    db.commit()




def is_token_valid(db: Session, user_id: int, token: str) -> bool:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_db = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False
        ).first()
    return token_db is not None