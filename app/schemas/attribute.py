from pydantic import BaseModel, ConfigDict


class AttributeCreate(BaseModel):
    name: str
    value: str


class AttributeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = None
    value: str | None = None


class AttributeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_attribute_id: int
    product_id: int
    name: str
    value: str
