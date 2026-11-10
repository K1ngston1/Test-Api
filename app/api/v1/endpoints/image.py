from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import product_dep
from core.database import get_db
from models import Product
from schemas.image import ImageCreate, ImageOut, ImageUpdate
from services import image as service

router = APIRouter(prefix="/product/{product_id}/image", tags=["product image"])


@router.get("", response_model=list[ImageOut])
def list_images(product: Product = Depends(product_dep)):
    return product.images


@router.get("/{product_image_id}", response_model=ImageOut)
def get_image(product_image_id: int, product: Product = Depends(product_dep),
              db: Session = Depends(get_db)):
    return service.get_image(db, product, product_image_id)


@router.post("", response_model=ImageOut, status_code=status.HTTP_201_CREATED)
def add_image(data: ImageCreate, product: Product = Depends(product_dep),
              db: Session = Depends(get_db)):
    return service.add_image(db, product, data)


@router.patch("/{product_image_id}", response_model=ImageOut)
def update_image(product_image_id: int, data: ImageUpdate,
                 product: Product = Depends(product_dep), db: Session = Depends(get_db)):
    return service.update_image(db, product, product_image_id, data)


@router.delete("/{product_image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(product_image_id: int, product: Product = Depends(product_dep),
                 db: Session = Depends(get_db)):
    service.delete_image(db, product, product_image_id)
