from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.category_id", name="fk_category_parent"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255))
