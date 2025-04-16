from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# Base schema
class PartOptionBase(BaseModel):
    name: str
    base_price: Decimal
    is_in_stock: Optional[bool] = True
    part_category_id: int

# Schema for creation
class PartOptionCreate(PartOptionBase):
    pass

# Schema for update
class PartOptionUpdate(BaseModel):
    name: Optional[str] = None
    base_price: Optional[Decimal] = None
    is_in_stock: Optional[bool] = None
    # part_category_id: Optional[int] = None # Should changing category be allowed?

# Schema for reading
class PartOption(PartOptionBase):
    id: int

    class Config:
        from_attributes = True 