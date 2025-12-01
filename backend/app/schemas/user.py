# app/schemas/user.py

from enum import Enum

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    OPERATOR = "OPERATOR"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRole(BaseModel):
    """
    Schéma pour changer le rôle d'un utilisateur (ADMIN only).
    """
    role: UserRole
