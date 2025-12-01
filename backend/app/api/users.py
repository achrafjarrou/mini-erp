# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdateRole
from app.auth.auth_bearer import JWTBearer             # ⬅️ CORRECT
from app.auth.jwt_handler import decode_access_token   # ⬅️ UTILISÉ POUR DÉCODER JWT
from app.services.user_service import (
    create_user,
    get_all_users,
    change_user_role,
    get_user_by_email,
)

router = APIRouter(prefix="/users", tags=["users"])


# ---------------------------------------------------------
# 🔵 Create User
# ---------------------------------------------------------
@router.post("/", response_model=UserResponse, status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)


# ---------------------------------------------------------
# 🟢 Get logged user (/users/me)
# ---------------------------------------------------------
@router.get("/me", response_model=UserResponse, dependencies=[Depends(JWTBearer())])
def get_me(
    token: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    token_data = decode_access_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
        )

    user = get_user_by_email(db, token_data.sub)
    return user


# ---------------------------------------------------------
# 🟡 List all users (ADMIN only)
# ---------------------------------------------------------
@router.get("/", response_model=list[UserResponse], dependencies=[Depends(JWTBearer("ADMIN"))])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# ---------------------------------------------------------
# 🔴 Change role (ADMIN only)
# ---------------------------------------------------------
@router.patch("/{user_id}/role", response_model=UserResponse, dependencies=[Depends(JWTBearer("ADMIN"))])
def update_role(
    user_id: int,
    role_data: UserUpdateRole,
    db: Session = Depends(get_db),
):
    return change_user_role(db, user_id, role_data.role)
