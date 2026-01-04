from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True
