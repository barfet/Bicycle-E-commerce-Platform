from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.part_category import PartCategory
from app.schemas.part_category import PartCategoryCreate, PartCategoryUpdate

async def get_part_category(db: AsyncSession, part_category_id: int) -> Optional[PartCategory]:
    """Get a single part category by ID."""
    return await db.get(PartCategory, part_category_id)

async def get_part_categories_by_product_type(
    db: AsyncSession, product_type_id: int, skip: int = 0, limit: int = 100
) -> List[PartCategory]:
    """Get a list of part categories for a specific product type."""
    statement = (
        select(PartCategory)
        .where(PartCategory.product_type_id == product_type_id)
        .order_by(PartCategory.display_order) # Order by display_order
        .offset(skip)
        .limit(limit)
    )
    result = await db.scalars(statement)
    return list(result.all())

async def create_part_category(db: AsyncSession, part_category_in: PartCategoryCreate) -> PartCategory:
    """Create a new part category linked to a product type."""
    # Ensure product_type_id exists? Or rely on DB foreign key constraint?
    # Relying on FK constraint for now.
    db_part_category = PartCategory(**part_category_in.model_dump())
    db.add(db_part_category)
    await db.commit()
    await db.refresh(db_part_category)
    return db_part_category

async def update_part_category(
    db: AsyncSession, db_obj: PartCategory, part_category_in: PartCategoryUpdate
) -> PartCategory:
    """Update an existing part category."""
    update_data = part_category_in.model_dump(exclude_unset=True)
    # TODO: Validate product_type_id if it's being changed?
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove_part_category(db: AsyncSession, part_category_id: int) -> Optional[PartCategory]:
    """Delete a part category by ID."""
    # Note: Cascade delete should handle removing associated PartOptions
    db_obj = await db.get(PartCategory, part_category_id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
    return db_obj 