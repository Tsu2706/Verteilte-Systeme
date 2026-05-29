import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 Stunden

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

# Pflicht-Login: Wenn kein Token vorhanden ist, kommt direkt 401
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Optionaler Login: Wenn kein Token vorhanden ist, kommt NICHT direkt 401
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="token",
    auto_error=False
)


def get_password_hash(plain_password: str) -> str:
    """Erzeugt einen Argon2-Hash inkl. automatisch eingebettetem Salt."""
    return password_hash.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vergleicht ein Klartext-Passwort mit einem gespeicherten Hash."""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    """Erzeugt einen signierten JWT mit Ablaufzeit."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(
        {"sub": username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> str:
    """
    Pflicht-Login:
    Validiert den Bearer-Token und gibt den Benutzernamen zurück.
    Wird für geschützte Endpunkte verwendet.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        return username

    except InvalidTokenError:
        raise credentials_exception


async def get_current_user_optional(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
) -> str | None:
    """
    Optionaler Login:
    Gibt None zurück, wenn kein Token vorhanden ist.
    Wird für öffentliche Endpunkte verwendet.
    """
    if token is None:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        return username

    except InvalidTokenError:
        raise credentials_exception
