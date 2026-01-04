from sqlalchemy.orm import Session
from models.product import Product

def get_all(db: Session):
    return db.query(Product).all()

def get_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update(db: Session, product: Product):
    db.commit()
    db.refresh(product)
    return product

def delete(db: Session, product: Product):
    db.delete(product)
    db.commit()
