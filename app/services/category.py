from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Category, Product, ProductCategory
from schemas.category import CategoryOut, ProductCategoryOut


def build_category_map(db: Session) -> dict[int, tuple[str, int | None]]:
    rows = db.execute(
        select(Category.category_id, Category.name, Category.parent_category_id)
    ).all()
    return {r.category_id: (r.name, r.parent_category_id) for r in rows}


def build_path(cmap: dict, category_id: int) -> str:
    parts, seen = [], set()
    while category_id and category_id in cmap and category_id not in seen:
        seen.add(category_id)
        name, parent = cmap[category_id]
        parts.append(name)
        category_id = parent
    return " > ".join(reversed(parts))


def category_out(cmap: dict, category_id: int) -> CategoryOut:
    return CategoryOut(
        category_id=category_id,
        name=cmap.get(category_id, ("", None))[0],
        path=build_path(cmap, category_id),
    )


def product_category_out(cmap: dict, pc: ProductCategory) -> ProductCategoryOut:
    return ProductCategoryOut(
        product_category_id=pc.product_category_id,
        **category_out(cmap, pc.category_id).model_dump(),
    )


def ensure_categories_exist(db: Session, ids: list[int]) -> None:
    ids = set(ids)
    if not ids:
        return
    found = set(db.scalars(select(Category.category_id).where(Category.category_id.in_(ids))))
    if missing := ids - found:
        raise HTTPException(404, f"Categories not found: {sorted(missing)}")


def list_product_categories(db: Session, product: Product):
    cmap = build_category_map(db)
    return [product_category_out(cmap, pc) for pc in product.product_categories]


def get_product_category(db: Session, product: Product, product_category_id: int):
    pc = db.get(ProductCategory, product_category_id)
    if not pc or pc.product_id != product.product_id:
        raise HTTPException(404, "Product category not found")
    return pc


def add_product_category(db: Session, product: Product, category_id: int):
    ensure_categories_exist(db, [category_id])
    if any(pc.category_id == category_id for pc in product.product_categories):
        raise HTTPException(409, "Category already linked to product")
    pc = ProductCategory(product_id=product.product_id, category_id=category_id)
    db.add(pc)
    db.commit()
    db.refresh(pc)
    return product_category_out(build_category_map(db), pc)


def delete_product_category(db: Session, product: Product, product_category_id: int):
    db.delete(get_product_category(db, product, product_category_id))
    db.commit()
