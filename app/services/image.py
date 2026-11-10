from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Product, ProductImage
from schemas.image import ImageCreate, ImageUpdate


def get_image(db: Session, product: Product, image_id: int) -> ProductImage:
    img = db.get(ProductImage, image_id)
    if not img or img.product_id != product.product_id:
        raise HTTPException(404, "Image not found")
    return img


def add_image(db: Session, product: Product, data: ImageCreate) -> ProductImage:
    img = ProductImage(product_id=product.product_id, **data.model_dump())
    db.add(img)
    db.commit()
    db.refresh(img)
    return img


def update_image(db: Session, product: Product, image_id: int, data: ImageUpdate):
    img = get_image(db, product, image_id)
    img.sort_order = data.sort_order
    db.commit()
    db.refresh(img)
    return img


def delete_image(db: Session, product: Product, image_id: int) -> None:
    db.delete(get_image(db, product, image_id))
    db.commit()
