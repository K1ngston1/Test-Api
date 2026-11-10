from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Product, ProductStore, Store
from schemas.store import ProductStoreOut


def to_out(ps: ProductStore) -> ProductStoreOut:
    return ProductStoreOut(
        product_store_id=ps.product_store_id, store_id=ps.store_id, name=ps.store.name
    )


def ensure_stores_exist(db: Session, ids: list[int]) -> None:
    ids = set(ids)
    if not ids:
        return
    found = set(db.scalars(select(Store.store_id).where(Store.store_id.in_(ids))))
    if missing := ids - found:
        raise HTTPException(404, f"Stores not found: {sorted(missing)}")


def get_product_store(db: Session, product: Product, product_store_id: int) -> ProductStore:
    ps = db.get(ProductStore, product_store_id)
    if not ps or ps.product_id != product.product_id:
        raise HTTPException(404, "Product store not found")
    return ps


def add_product_store(db: Session, product: Product, store_id: int) -> ProductStoreOut:
    ensure_stores_exist(db, [store_id])
    if any(ps.store_id == store_id for ps in product.product_stores):
        raise HTTPException(409, "Store already linked to product")
    ps = ProductStore(product_id=product.product_id, store_id=store_id)
    db.add(ps)
    db.commit()
    db.refresh(ps)
    return to_out(ps)


def delete_product_store(db: Session, product: Product, product_store_id: int) -> None:
    db.delete(get_product_store(db, product, product_store_id))
    db.commit()
