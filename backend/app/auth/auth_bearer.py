# app/auth/auth_bearer.py

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt_handler import decode_access_token


class JWTBearer(HTTPBearer):
    def __init__(self, required_role: str = None, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.required_role = required_role

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            token = credentials.credentials
            payload = decode_access_token(token)

            if payload is None:
                raise HTTPException(status_code=403, detail="Token invalide")

            # Check role if required
            if self.required_role and payload.role != self.required_role:
                raise HTTPException(status_code=403, detail="Accès refusé (rôle insuffisant)")

            # SUCCESS → return token
            return token

        raise HTTPException(status_code=403, detail="Token non fourni")
