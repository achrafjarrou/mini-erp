# app/auth/roles.py

from fastapi import Depends, HTTPException, status
from app.auth.auth_bearer import get_current_user
from app.models.user import User

def require_role(*allowed_roles: str):

    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas la permission d'accéder à cette ressource.",
            )
        return current_user

    return role_dependency
