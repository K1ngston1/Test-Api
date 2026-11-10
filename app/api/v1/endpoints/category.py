from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import product_dep
from core.database import get_db
from models import Product
from schemas.category import CategoryLink, ProductCategoryOut
from services import category as service

router = APIRouter(prefix="/product/{product_id}/category", tags=["product category"])


@router.get("", response_model=list[ProductCategoryOut])
def list_categories(product: Product = Depends(product_dep), db: Session = Depends(get_db)):
    return service.list_product_categories(db, product)


@router.get("/{product_category_id}", response_model=ProductCategoryOut)
def get_category(product_category_id: int, product: Product = Depends(product_dep),
                 db: Session = Depends(get_db)):
    pc = service.get_product_category(db, product, product_category_id)
    return service.product_category_out(service.build_category_map(db), pc)


@router.post("", response_model=ProductCategoryOut, status_code=status.HTTP_201_CREATED)
def add_category(data: CategoryLink, product: Product = Depends(product_dep),
                 db: Session = Depends(get_db)):
    return service.add_product_category(db, product, data.category_id)


@router.delete("/{product_category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(product_category_id: int, product: Product = Depends(product_dep),
                    db: Session = Depends(get_db)):
    service.delete_product_category(db, product, product_category_id)
