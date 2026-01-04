from sqlalchemy.orm import Session
from models.user import User


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def count_all(db: Session):
    return db.query(User).count()


def create(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user


def get_all(db: Session):
    return db.query(User).all()


def delete(db: Session, user: User):
    db.delete(user)
    db.commit()
    return True