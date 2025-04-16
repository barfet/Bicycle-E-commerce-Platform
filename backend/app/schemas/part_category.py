from pydantic import BaseModel
from typing import Optional

# Base schema
class PartCategoryBase(BaseModel):
    name: str
    display_order: Optional[int] = 0
    product_type_id: int

# Schema for creation
class PartCategoryCreate(PartCategoryBase):
    pass

# Schema for update
class PartCategoryUpdate(PartCategoryBase):
    name: Optional[str] = None
    display_order: Optional[int] = None
    product_type_id: Optional[int] = None # Allow changing association?

# Schema for reading
class PartCategory(PartCategoryBase):
    id: int

    class Config:
        from_attributes = True 