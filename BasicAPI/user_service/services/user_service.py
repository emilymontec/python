from sqlalchemy.orm import Session
from repositories import user_repository
from fastapi import HTTPException
from models.user import Role

def list_users(db: Session):
    try:
        users = user_repository.get_all(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

def get_user(db: Session, user_id: int):
    try:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

def update_user_role(db: Session, user_id: int, new_role: Role):
    try:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            return None
        user.role = new_role
        return user_repository.update(db, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user role: {str(e)}")

def delete_user(db: Session, user_id: int):
    try:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            return None
        user_repository.delete(db, user)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")