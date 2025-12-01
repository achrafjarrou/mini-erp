from pydantic import BaseModel, EmailStr
from typing import Optional

# -----------------------------
# POUR LOGIN
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -----------------------------
# POUR TOKEN
# -----------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None   # email
    role: Optional[str] = None  # rôle associé
