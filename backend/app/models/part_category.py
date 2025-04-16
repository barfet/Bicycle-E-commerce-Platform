from sqlalchemy import String, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from app.db.base import Base

class PartCategory(Base):
    __tablename__ = "part_categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_types.id"))

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # Relationships
    product_type: Mapped["ProductType"] = relationship(back_populates="part_categories")
    part_options: Mapped[List["PartOption"]] = relationship(back_populates="part_category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<PartCategory(id={self.id}, name='{self.name}', product_type_id={self.product_type_id})>" 