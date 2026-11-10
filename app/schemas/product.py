from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from schemas.attribute import AttributeCreate, AttributeOut
from schemas.category import CategoryOut, ProductCategoryOut
from schemas.image import ImageCreate, ImageOut
from schemas.store import ProductStoreOut


class ManufacturerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    manufacturer_id: int
    name: str
    image: str | None = None


# ---- list ----
class ProductListItem(BaseModel):
    product_id: int
    name: str
    price: Decimal
    categories: list[CategoryOut]


class ProductListResponse(BaseModel):
    items: list[ProductListItem]
    total: int
    page: int
    limit: int
    pages: int


# ---- detail ----
class ProductDetail(BaseModel):
    product_id: int
    name: str
    model: str | None
    description: str | None
    image: str | None
    price: Decimal
    status: int
    manufacturer_id: int | None
    date_added: datetime
    date_modify: datetime
    categories: list[ProductCategoryOut]
    attributes: list[AttributeOut]
    images: list[ImageOut]
    stores: list[ProductStoreOut]
    manufacturer: ManufacturerOut | None


# ---- create / update ----
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)  # обов'язкове
    status: int = 0                                  # за замовчуванням 0
    model: str | None = None
    description: str | None = None
    image: str | None = None
    price: Decimal = Decimal("0")
    manufacturer_id: int | None = None
    categories: list[int] = []
    attributes: list[AttributeCreate] = []
    images: list[ImageCreate] = []
    stores: list[int] = []


class ProductUpdate(BaseModel):
    """product_id, date_added, date_modify не редагуються (extra=forbid -> 422)."""
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: int | None = None
    model: str | None = None
    description: str | None = None
    image: str | None = None
    price: Decimal | None = None
    manufacturer_id: int | None = None
