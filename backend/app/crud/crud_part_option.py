from sqlalchemy.orm import Session # Keep for potential sync usage elsewhere? Or remove if fully async
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.part_option import PartOption
from app.schemas.part_option import PartOptionCreate, PartOptionUpdate

# Use AsyncSession and make functions async
async def get_part_option(db: AsyncSession, part_option_id: int) -> Optional[PartOption]:
    """Get a single part option by ID."""
    # db.get is sync, use db.get with await for async
    return await db.get(PartOption, part_option_id)

async def get_part_options_by_category(
    db: AsyncSession, part_category_id: int, skip: int = 0, limit: int = 100
) -> List[PartOption]:
    """Get a list of part options for a specific category."""
    statement = (
        select(PartOption)
        .where(PartOption.part_category_id == part_category_id)
        # Consider adding an order_by, e.g., by name or id
        .order_by(PartOption.name)
        .offset(skip)
        .limit(limit)
    )
    # Use await db.scalars for async execution
    result = await db.scalars(statement)
    return list(result.all())

async def create_part_option(db: AsyncSession, part_option_in: PartOptionCreate) -> PartOption:
    """Create a new part option linked to a category."""
    # Relying on FK constraint for part_category_id validation
    db_part_option = PartOption(**part_option_in.model_dump())
    db.add(db_part_option)
    # Use await for commit and refresh
    await db.commit()
    await db.refresh(db_part_option)
    return db_part_option

async def update_part_option(
    db: AsyncSession, db_obj: PartOption, part_option_in: PartOptionUpdate
) -> PartOption:
    """Update an existing part option."""
    update_data = part_option_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    # Use await for commit and refresh
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove_part_option(db: AsyncSession, part_option_id: int) -> Optional[PartOption]:
    """Delete a part option by ID."""
    db_obj = await db.get(PartOption, part_option_id)
    if db_obj:
        # Use await for delete and commit
        await db.delete(db_obj)
        await db.commit()
    return db_obj 