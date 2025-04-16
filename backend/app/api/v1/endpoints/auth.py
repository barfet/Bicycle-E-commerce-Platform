from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import get_db
from app.core.security import create_access_token

router = APIRouter()

@router.post("/admin/login", response_model=schemas.Token)
def login_admin_for_access_token(
    form_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate admin user and return JWT token."""
    admin_user = crud.authenticate_admin_user(
        db,
        username=form_data.username,
        password=form_data.password
    )
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        subject=admin_user.username # Or admin_user.id
    )
    return {"access_token": access_token, "token_type": "bearer"} 