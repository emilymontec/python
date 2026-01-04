from pydantic import BaseModel
from models.user import Role

class UpdateRoleSchema(BaseModel):
    role: Role

class UserOut(BaseModel):
    id: int
    email: str
    role: Role

    class Config:
        from_attributes = True
