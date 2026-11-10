from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Manufacturer(Base):
    __tablename__ = "manufacturer"

    manufacturer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
