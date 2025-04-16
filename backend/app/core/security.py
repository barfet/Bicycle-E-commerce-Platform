import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.config import settings

def hash_password(plain_password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    # Generate a salt and hash the password
    hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8') # Return the hash as a string

def check_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- JWT Token functions --- 
def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Function to decode/verify token will be needed in middleware (STORY-203)
def verify_token(token: str, credentials_exception: HTTPException) -> str:
    """Verifies a JWT token and returns the subject (e.g., username)."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Optionally, add more validation here (e.g., check token scope/type)
        return username
    except JWTError:
        raise credentials_exception 