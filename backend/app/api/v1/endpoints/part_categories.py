from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.api.deps import get_current_admin_user

router = APIRouter()

@router.post("/part-categories", response_model=schemas.PartCategory, status_code=status.HTTP_201_CREATED)
def create_new_part_category(
    *, # Keyword-only args
    db: Session = Depends(get_db),
    part_category_in: schemas.PartCategoryCreate,
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Create a new part category (requires admin privileges)."""
    # Check if product type exists first?
    product_type = crud.get_product_type(db, product_type_id=part_category_in.product_type_id)
    if not product_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ProductType with id {part_category_in.product_type_id} not found.",
        )
    try:
        part_category = crud.create_part_category(db=db, part_category_in=part_category_in)
    except IntegrityError: # Catch potential DB errors if constraints fail
        db.rollback()
        # Could be more specific, e.g., unique constraint on (product_type_id, name)?
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Part category creation failed. Check constraints.",
        )
    return part_category

@router.get("/part-categories", response_model=List[schemas.PartCategory])
def read_part_categories(
    db: Session = Depends(get_db),
    product_type_id: int | None = Query(None, description="Filter by Product Type ID"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Retrieve part categories, optionally filtered by ProductType (requires admin privileges)."""
    if product_type_id is not None:
        part_categories = crud.get_part_categories_by_product_type(
            db, product_type_id=product_type_id, skip=skip, limit=limit
        )
    else:
        # TODO: Implement get_all_part_categories if needed, or require product_type_id filter.
        # For now, returning empty list if no filter provided.
        # Alternatively, raise an error if product_type_id is mandatory.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'product_type_id' is required."
        )
        # part_categories = [] # Or implement a get_all function
    return part_categories

@router.get("/part-categories/{part_category_id}", response_model=schemas.PartCategory)
def read_part_category(
    part_category_id: int,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Retrieve a specific part category by ID (requires admin privileges)."""
    db_part_category = crud.get_part_category(db, part_category_id=part_category_id)
    if db_part_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartCategory not found")
    return db_part_category

@router.put("/part-categories/{part_category_id}", response_model=schemas.PartCategory)
def update_existing_part_category(
    part_category_id: int,
    part_category_in: schemas.PartCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Update a part category (requires admin privileges)."""
    db_part_category = crud.get_part_category(db, part_category_id=part_category_id)
    if not db_part_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartCategory not found")
    # If product_type_id is being changed, check if the new one exists
    if part_category_in.product_type_id is not None and \
       part_category_in.product_type_id != db_part_category.product_type_id:
        product_type = crud.get_product_type(db, product_type_id=part_category_in.product_type_id)
        if not product_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ProductType with id {part_category_in.product_type_id} not found.",
            )
    try:
        updated_part_category = crud.update_part_category(
            db=db, db_obj=db_part_category, part_category_in=part_category_in
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Part category update failed. Check constraints.",
        )
    return updated_part_category

@router.delete("/part-categories/{part_category_id}", response_model=schemas.PartCategory)
def delete_part_category(
    part_category_id: int,
    db: Session = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Delete a part category (requires admin privileges)."""
    deleted_part_category = crud.remove_part_category(db=db, part_category_id=part_category_id)
    if not deleted_part_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartCategory not found")
    return deleted_part_category 