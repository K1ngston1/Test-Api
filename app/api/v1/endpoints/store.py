from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import product_dep
from core.database import get_db
from models import Product
from schemas.store import ProductStoreOut, StoreLink
from services import store as service

router = APIRouter(prefix="/product/{product_id}/store", tags=["product store"])


@router.get("", response_model=list[ProductStoreOut])
def list_stores(product: Product = Depends(product_dep)):
    return [service.to_out(ps) for ps in product.product_stores]


@router.get("/{product_store_id}", response_model=ProductStoreOut)
def get_store(product_store_id: int, product: Product = Depends(product_dep),
              db: Session = Depends(get_db)):
    return service.to_out(service.get_product_store(db, product, product_store_id))


@router.post("", response_model=ProductStoreOut, status_code=status.HTTP_201_CREATED)
def add_store(data: StoreLink, product: Product = Depends(product_dep),
              db: Session = Depends(get_db)):
    return service.add_product_store(db, product, data.store_id)


@router.delete("/{product_store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(product_store_id: int, product: Product = Depends(product_dep),
                 db: Session = Depends(get_db)):
    service.delete_product_store(db, product, product_store_id)
