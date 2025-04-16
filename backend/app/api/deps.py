from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import crud, models
from app.core.security import verify_token
from app.db.session import get_db

# Define the OAuth2 scheme
# tokenUrl should point to our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")

# Define the credentials exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_admin_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.AdminUser:
    """Dependency to get the current authenticated admin user."""
    username = verify_token(token=token, credentials_exception=credentials_exception)
    user = crud.get_admin_user_by_username(db, username=username)
    if user is None:
        # This case might happen if the user was deleted after the token was issued
        raise credentials_exception
    return user 