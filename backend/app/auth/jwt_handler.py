from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings
from app.schemas.auth import TokenData


def create_access_token(sub: str, role: str):
    """
    Crée un JWT avec email + rôle + expiration.
    """
    payload = {
        "sub": sub,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str):
    """
    Décode un token JWT. Retourne TokenData si OK, None sinon.
    """
    try:
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return TokenData(
            sub=decoded.get("sub"),
            role=decoded.get("role")
        )

    except JWTError:
        return None
