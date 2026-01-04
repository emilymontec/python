from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.auth_services import login, register
from schemas.auth import LoginSchema, RegisterSchema
from repositories import user_repository


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user(data: RegisterSchema, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = user_repository.get_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        user = register(db, data.email, data.password, data.role)
        return {"id": user.id, "email": user.email, "role": user.role.value}
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        # Si es un error de integridad (email duplicado), dar mensaje más claro
        if "UNIQUE constraint" in error_msg or "unique constraint" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=500, detail=f"Error registering user: {error_msg}")


@router.post("/login")
def login_user(data: LoginSchema, db: Session = Depends(get_db)):
    try:
        result = login(db, data.email, data.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": result[0], "refresh_token": result[1]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")