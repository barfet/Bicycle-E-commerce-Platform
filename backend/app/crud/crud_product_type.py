from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update, delete as sql_delete
from typing import List, Optional

from app.models.product_type import ProductType
from app.schemas.product_type import ProductTypeCreate, ProductTypeUpdate

async def get_product_type(db: AsyncSession, product_type_id: int) -> Optional[ProductType]:
    """Get a single product type by ID."""
    return await db.get(ProductType, product_type_id)

async def get_product_types(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProductType]:
    """Get a list of product types with pagination."""
    statement = select(ProductType).offset(skip).limit(limit)
    result = await db.scalars(statement)
    return list(result.all())

async def create_product_type(db: AsyncSession, product_type_in: ProductTypeCreate) -> ProductType:
    """Create a new product type."""
    db_product_type = ProductType(**product_type_in.model_dump())
    db.add(db_product_type)
    await db.commit()
    await db.refresh(db_product_type)
    return db_product_type

async def update_product_type(
    db: AsyncSession, db_obj: ProductType, product_type_in: ProductTypeUpdate
) -> ProductType:
    """Update an existing product type."""
    update_data = product_type_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove_product_type(db: AsyncSession, product_type_id: int) -> Optional[ProductType]:
    """Delete a product type by ID."""
    db_obj = await db.get(ProductType, product_type_id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
    return db_obj 