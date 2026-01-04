from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.product_service import list_products, create_product, update_product, delete_product as delete_product_service
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from dependencies.auth import require_roles
from middlewares.rate_limit import rate_limit

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
@rate_limit("products_read", limit=100, window=3600)
def list_products_endpoint(db: Session = Depends(get_db)):
    return list_products(db)

@router.post("/", response_model=ProductOut)
@rate_limit("products_write", limit=20, window=3600)
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "manager"))
):
    return create_product(db, product)

@router.patch("/{product_id}", response_model=ProductOut)
@rate_limit("products_write", limit=20, window=3600)
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "manager"))
):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    deleted = delete_product_service(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Deleted"}
