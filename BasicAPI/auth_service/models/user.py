from sqlalchemy import Column, Integer, String, Enum
from database import Base
from enum import Enum as PyEnum


class Role(PyEnum):
    admin = "admin"
    manager = "manager"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.user)