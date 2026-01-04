from sqlalchemy.orm import Session
from repositories import product_repository
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate

def list_products(db: Session):
    return product_repository.get_all(db)

def create_product(db: Session, data: ProductCreate):
    product = Product(**data.model_dump())
    return product_repository.create(db, product)

def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = product_repository.get_by_id(db, product_id)
    if not product:
        return None
    
    # Actualizar solo los campos que se proporcionaron
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    return product_repository.update(db, product)

def delete_product(db: Session, product_id: int):
    product = product_repository.get_by_id(db, product_id)
    if not product:
        return None
    product_repository.delete(db, product)
    return product
