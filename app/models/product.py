from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, SmallInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.category import Category
from models.manufacture import Manufacturer
from models.store import Store

_CASCADE = "all, delete-orphan"


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[int | None] = mapped_column(
        ForeignKey("manufacturer.manufacturer_id", name="fk_product_manufacturer"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255))
    model: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 4), default=0)
    status: Mapped[int] = mapped_column(SmallInteger, default=0)
    date_added: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    date_modify: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    manufacturer: Mapped[Manufacturer | None] = relationship()
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product", cascade=_CASCADE, order_by="ProductImage.sort_order"
    )
    attributes: Mapped[list["ProductAttribute"]] = relationship(
        back_populates="product", cascade=_CASCADE
    )
    product_categories: Mapped[list["ProductCategory"]] = relationship(
        back_populates="product", cascade=_CASCADE
    )
    product_stores: Mapped[list["ProductStore"]] = relationship(
        back_populates="product", cascade=_CASCADE
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    product_image_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", name="fk_image_product")
    )
    image: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)

    product: Mapped[Product] = relationship(back_populates="images")


class ProductAttribute(Base):
    __tablename__ = "product_attribute"

    product_attribute_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", name="fk_attribute_product")
    )
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(Text)

    product: Mapped[Product] = relationship(back_populates="attributes")


class ProductCategory(Base):
    __tablename__ = "product_category"

    product_category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", name="fk_pc_product")
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", name="fk_pc_category")
    )

    product: Mapped[Product] = relationship(back_populates="product_categories")
    category: Mapped[Category] = relationship()


class ProductStore(Base):
    __tablename__ = "product_store"

    product_store_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", name="fk_ps_product")
    )
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id", name="fk_ps_store"))

    product: Mapped[Product] = relationship(back_populates="product_stores")
    store: Mapped[Store] = relationship()
