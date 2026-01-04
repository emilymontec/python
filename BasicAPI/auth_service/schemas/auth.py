from pydantic import BaseModel
from models.user import Role
from typing import Optional

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: str
    password: str
    role: Optional[Role] = None  # Si no se especifica, será "user" por defecto

class UpdateRoleSchema(BaseModel):
    role: Role

class UserOut(BaseModel):
    id: int
    email: str
    role: Role

    class Config:
        from_attributes = True