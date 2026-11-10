from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Product, ProductAttribute
from schemas.attribute import AttributeCreate, AttributeUpdate


def get_attribute(db: Session, product: Product, attribute_id: int) -> ProductAttribute:
    attr = db.get(ProductAttribute, attribute_id)
    if not attr or attr.product_id != product.product_id:
        raise HTTPException(404, "Attribute not found")
    return attr


def add_attribute(db: Session, product: Product, data: AttributeCreate):
    attr = ProductAttribute(product_id=product.product_id, **data.model_dump())
    db.add(attr)
    db.commit()
    db.refresh(attr)
    return attr


def update_attribute(db: Session, product: Product, attribute_id: int, data: AttributeUpdate):
    attr = get_attribute(db, product, attribute_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(attr, key, value)
    db.commit()
    db.refresh(attr)
    return attr


def delete_attribute(db: Session, product: Product, attribute_id: int) -> None:
    db.delete(get_attribute(db, product, attribute_id))
    db.commit()
