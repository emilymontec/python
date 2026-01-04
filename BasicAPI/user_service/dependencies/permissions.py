from fastapi import Depends, HTTPException, status
from dependencies.auth import get_current_user

def require_roles(*roles):
    def checker(user=Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return checker
