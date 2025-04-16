from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from app.db.base import Base

class ProductType(Base):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # Relationships
    part_categories: Mapped[List["PartCategory"]] = relationship(back_populates="product_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ProductType(id={self.id}, name='{self.name}')>" 