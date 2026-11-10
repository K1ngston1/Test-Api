from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.product import (
    ProductCreate, ProductDetail, ProductListResponse, ProductUpdate,
)
from services import product as service

router = APIRouter(prefix="/product", tags=["product"])


@router.get("", response_model=ProductListResponse)
def list_products(
    category_id: int | None = None,
    price_from: Decimal | None = Query(None, ge=0),
    price_to: Decimal | None = Query(None, ge=0),
    sort_by: Literal["name", "price", "category"] = "name",
    order: Literal["asc", "desc"] = "asc",  # asc: А→Я, desc: Я→А
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_products(
        db, category_id=category_id, price_from=price_from, price_to=price_to,
        sort_by=sort_by, order=order, page=page, limit=limit,
    )


@router.get("/{product_id}", response_model=ProductDetail)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_product_detail(db, product_id)


@router.post("", response_model=ProductDetail, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, data)


@router.patch("/{product_id}", response_model=ProductDetail)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    return service.update_product(db, product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service.delete_product(db, product_id)
