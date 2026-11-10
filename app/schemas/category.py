from pydantic import BaseModel


class CategoryLink(BaseModel):
    category_id: int


class CategoryOut(BaseModel):
    category_id: int
    name: str
    path: str  # повний шлях: "Електроніка > Телефони > Смартфони"


class ProductCategoryOut(CategoryOut):
    product_category_id: int
