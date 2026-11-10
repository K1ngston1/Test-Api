from pydantic import BaseModel


class StoreLink(BaseModel):
    store_id: int


class ProductStoreOut(BaseModel):
    product_store_id: int
    store_id: int
    name: str
