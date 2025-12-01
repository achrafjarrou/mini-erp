from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import Token, UserLogin
from app.auth.jwt_handler import create_access_token
from app.services.user_service import authenticate_user

router = APIRouter()


@router.post("/auth/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(sub=user.email, role=user.role)
    return {"access_token": token, "token_type": "bearer"}
