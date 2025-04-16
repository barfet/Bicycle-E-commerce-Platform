from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.api.deps import get_current_admin_user

router = APIRouter()

@router.post("/part-options", response_model=schemas.PartOption, status_code=status.HTTP_201_CREATED)
async def create_new_part_option(
    *,
    db: AsyncSession = Depends(get_db),
    part_option_in: schemas.PartOptionCreate,
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Create a new part option (requires admin privileges)."""
    # Check if part category exists
    part_category = await crud.get_part_category(db, part_category_id=part_option_in.part_category_id)
    if not part_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PartCategory with id {part_option_in.part_category_id} not found.",
        )
    try:
        part_option = await crud.create_part_option(db=db, part_option_in=part_option_in)
    except IntegrityError: # Catch potential DB errors
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Part option creation failed. Check constraints.",
        )
    return part_option

@router.get("/part-options", response_model=List[schemas.PartOption])
async def read_part_options(
    db: AsyncSession = Depends(get_db),
    part_category_id: int | None = Query(None, description="Filter by Part Category ID"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Retrieve part options, optionally filtered by PartCategory (requires admin privileges)."""
    if part_category_id is not None:
        part_options = await crud.get_part_options_by_category(
            db, part_category_id=part_category_id, skip=skip, limit=limit
        )
    else:
        # Require filtering by category
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'part_category_id' is required."
        )
    return part_options

@router.get("/part-options/{part_option_id}", response_model=schemas.PartOption)
async def read_part_option(
    part_option_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Retrieve a specific part option by ID (requires admin privileges)."""
    db_part_option = await crud.get_part_option(db, part_option_id=part_option_id)
    if db_part_option is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartOption not found")
    return db_part_option

@router.put("/part-options/{part_option_id}", response_model=schemas.PartOption)
async def update_existing_part_option(
    part_option_id: int,
    part_option_in: schemas.PartOptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Update a part option (price, stock, name) (requires admin privileges)."""
    db_part_option = await crud.get_part_option(db, part_option_id=part_option_id)
    if not db_part_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartOption not found")

    # Note: Not allowing changing part_category_id via this endpoint for simplicity
    if part_option_in.model_dump(exclude_unset=True).get('part_category_id') is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Changing the part category of an option is not allowed via this endpoint."
        )

    try:
        updated_part_option = await crud.update_part_option(
            db=db, db_obj=db_part_option, part_option_in=part_option_in
        )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Part option update failed. Check constraints.",
        )
    return updated_part_option

@router.delete("/part-options/{part_option_id}", response_model=schemas.PartOption)
async def delete_part_option(
    part_option_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.AdminUser = Depends(get_current_admin_user)
):
    """Delete a part option (requires admin privileges)."""
    deleted_part_option = await crud.remove_part_option(db=db, part_option_id=part_option_id)
    if not deleted_part_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PartOption not found")
    return deleted_part_option 