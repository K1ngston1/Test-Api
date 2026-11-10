from models.category import Category
from models.manufacture import Manufacturer   # назва файлу як у вас
from models.product import (
    Product,
    ProductAttribute,
    ProductCategory,
    ProductImage,
    ProductStore,
)
from models.store import Store

__all__ = [
    "Category", "Manufacturer", "Product", "ProductAttribute",
    "ProductCategory", "ProductImage", "ProductStore", "Store",
]