from sqlalchemy.orm import Session
from models.user import User

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user

def delete(db: Session, user: User):
    db.delete(user)
    db.commit()
    return True