from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import product_dep
from core.database import get_db
from models import Product
from schemas.attribute import AttributeCreate, AttributeOut, AttributeUpdate
from services import attribute as service

router = APIRouter(prefix="/product/{product_id}/attribute", tags=["product attribute"])


@router.get("", response_model=list[AttributeOut])
def list_attributes(product: Product = Depends(product_dep)):
    return product.attributes


@router.get("/{product_attribute_id}", response_model=AttributeOut)
def get_attribute(product_attribute_id: int, product: Product = Depends(product_dep),
                  db: Session = Depends(get_db)):
    return service.get_attribute(db, product, product_attribute_id)


@router.post("", response_model=AttributeOut, status_code=status.HTTP_201_CREATED)
def add_attribute(data: AttributeCreate, product: Product = Depends(product_dep),
                  db: Session = Depends(get_db)):
    return service.add_attribute(db, product, data)


@router.patch("/{product_attribute_id}", response_model=AttributeOut)
def update_attribute(product_attribute_id: int, data: AttributeUpdate,
                     product: Product = Depends(product_dep), db: Session = Depends(get_db)):
    return service.update_attribute(db, product, product_attribute_id, data)


@router.delete("/{product_attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attribute(product_attribute_id: int, product: Product = Depends(product_dep),
                     db: Session = Depends(get_db)):
    service.delete_attribute(db, product, product_attribute_id)
