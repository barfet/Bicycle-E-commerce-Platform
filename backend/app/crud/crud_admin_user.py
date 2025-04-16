from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from app.models.admin_user import AdminUser
from app.core.security import check_password

def get_admin_user_by_username(db: Session, username: str) -> Optional[AdminUser]:
    """Fetches an admin user by username."""
    statement = select(AdminUser).where(AdminUser.username == username)
    return db.scalars(statement).first()

def authenticate_admin_user(db: Session, username: str, password: str) -> Optional[AdminUser]:
    """Authenticates an admin user by username and password."""
    user = get_admin_user_by_username(db, username=username)
    if not user:
        return None
    if not check_password(password, user.password_hash):
        return None
    return user 