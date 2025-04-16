from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.api.deps import get_current_admin_user

router = APIRouter()

@router.post("/product-types", response_model=schemas.ProductType, status_code=status.HTTP_201_CREATED)
def create_new_product_type(
    *, # Make following arguments keyword-only
    db: Session = Depends(get_db),
    product_type_in: schemas.ProductTypeCreate,
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Create a new product type (requires admin privileges)."""
    try:
        product_type = crud.create_product_type(db=db, product_type_in=product_type_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"ProductType with name '{product_type_in.name}' already exists.",
        )
    return product_type

@router.get("/product-types", response_model=List[schemas.ProductType])
def read_product_types(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.AdminUser = Depends(get_current_admin_user) # Protect endpoint
):
    """Retrieve product types (requires admin privileges)."""
    product_types = crud.get_product_types(db, skip=skip, limit=limit)
    return product_types

@router.get("/product-types/{product_type_id}", response_model=schemas.ProductType)
def read_product_type(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user) # Protect endpoint
):
    """Retrieve a specific product type by ID (requires admin privileges)."""
    db_product_type = crud.get_product_type(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found")
    return db_product_type

@router.put("/product-types/{product_type_id}", response_model=schemas.ProductType)
def update_existing_product_type(
    product_type_id: int,
    product_type_in: schemas.ProductTypeUpdate,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Update a product type (requires admin privileges)."""
    db_product_type = crud.get_product_type(db, product_type_id=product_type_id)
    if not db_product_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found")
    # TODO: Handle potential duplicate name on update?
    updated_product_type = crud.update_product_type(
        db=db, db_obj=db_product_type, product_type_in=product_type_in
    )
    return updated_product_type

@router.delete("/product-types/{product_type_id}", response_model=schemas.ProductType)
def delete_product_type(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Delete a product type (requires admin privileges)."""
    deleted_product_type = crud.remove_product_type(db=db, product_type_id=product_type_id)
    if not deleted_product_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found")
    return deleted_product_type 