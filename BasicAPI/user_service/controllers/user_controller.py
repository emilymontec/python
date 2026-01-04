from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import list_users, get_user, update_user_role, delete_user
from dependencies.permissions import require_roles
from schemas.user import UserOut, UpdateRoleSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOut], summary="List all users")
def get_users(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    try:
        return list_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")


@router.get("/{user_id}", response_model=UserOut, summary="Get user by ID")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "manager"))
):
    return get_user(db, user_id)


@router.patch("/{user_id}/role", summary="Update user role", description="Update the role of a user")
def update_role(
    user_id: int,
    data: UpdateRoleSchema,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    updated = update_user_role(db, user_id, data.role)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Role updated successfully", "user_id": user_id, "new_role": data.role.value}


@router.delete("/{user_id}", summary="Delete user", description="Delete a user by ID")
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully", "user_id": user_id}
