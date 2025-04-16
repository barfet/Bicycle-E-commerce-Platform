from pydantic import BaseModel
from typing import Optional

# Base schema for common fields
class ProductTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema for creating a ProductType (request)
class ProductTypeCreate(ProductTypeBase):
    pass

# Schema for updating a ProductType (request)
class ProductTypeUpdate(ProductTypeBase):
    name: Optional[str] = None # Allow partial updates
    description: Optional[str] = None

# Schema for reading/returning a ProductType (response)
class ProductType(ProductTypeBase):
    id: int

    class Config:
        from_attributes = True # Allow creating schema from ORM model 