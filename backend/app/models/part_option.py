from sqlalchemy import String, Boolean, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base

class PartOption(Base):
    __tablename__ = "part_options"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    part_category_id: Mapped[int] = mapped_column(ForeignKey("part_categories.id"))

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # Relationships
    part_category: Mapped["PartCategory"] = relationship(back_populates="part_options")

    def __repr__(self) -> str:
        return f"<PartOption(id={self.id}, name='{self.name}', price={self.base_price}, category_id={self.part_category_id})>" 