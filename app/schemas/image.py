from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    image: str
    sort_order: int = 0


class ImageUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sort_order: int


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_image_id: int
    product_id: int
    image: str
    sort_order: int
