import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from models import (
    Category, Manufacturer,
    ProductStore,Product,
    ProductImage,
    ProductAttribute,
    ProductCategory,
)
from schemas.product import (
    ProductCreate, ProductDetail, ProductListItem, ProductListResponse, ProductUpdate,
)
from services import category as category_service
from services import store as store_service


def get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

def list_products(
    db: Session, *, category_id, price_from, price_to, sort_by, order, page, limit
) -> ProductListResponse:
    stmt = select(Product)
    if category_id is not None:
        stmt = stmt.where(
            Product.product_categories.any(ProductCategory.category_id == category_id)
        )
    if price_from is not None:
        stmt = stmt.where(Product.price >= price_from)
    if price_to is not None:
        stmt = stmt.where(Product.price <= price_to)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0

    if sort_by == "category":
        sort_col = (
            select(func.min(Category.name))
            .select_from(ProductCategory)
            .join(Category, Category.category_id == ProductCategory.category_id)
            .where(ProductCategory.product_id == Product.product_id)
            .correlate(Product)
            .scalar_subquery()
        )
    else:
        sort_col = {"name": Product.name, "price": Product.price}[sort_by]
    sort_col = sort_col.asc() if order == "asc" else sort_col.desc()

    stmt = (
        stmt.options(selectinload(Product.product_categories))
        .order_by(sort_col, Product.product_id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    products = db.scalars(stmt).all()

    cmap = category_service.build_category_map(db)
    items = [
        ProductListItem(
            product_id=p.product_id,
            name=p.name,
            price=p.price,
            categories=[
                category_service.category_out(cmap, pc.category_id)
                for pc in p.product_categories
            ],
        )
        for p in products
    ]
    return ProductListResponse(
        items=items, total=total, page=page, limit=limit, pages=math.ceil(total / limit)
    )
def get_product_detail(db: Session, product_id: int) -> ProductDetail:
    product = db.scalar(
        select(Product)
        .where(Product.product_id == product_id)
        .options(
            selectinload(Product.product_categories),
            selectinload(Product.attributes),
            selectinload(Product.images),
            selectinload(Product.product_stores).selectinload(ProductStore.store),
            selectinload(Product.manufacturer),
        )
    )
    if not product:
        raise HTTPException(404, "Product not found")

    cmap = category_service.build_category_map(db)
    return ProductDetail(
        product_id=product.product_id,
        name=product.name,
        model=product.model,
        description=product.description,
        image=product.image,
        price=product.price,
        status=product.status,
        manufacturer_id=product.manufacturer_id,
        date_added=product.date_added,
        date_modify=product.date_modify,
        categories=[category_service.product_category_out(cmap, pc) for pc in product.product_categories],
        attributes=product.attributes,
        images=product.images,
        stores=[store_service.to_out(ps) for ps in product.product_stores],
        manufacturer=product.manufacturer,
    )

def delete_product(db: Session, product_id: int) -> None:
    product = get_product_or_404(db, product_id)
    db.delete(product)  # cascade видаляє image/attribute/category/store зв'язки
    db.commit()


from sqlalchemy.exc import IntegrityError


def create_product(
    db: Session,
    product_id: int,
    data: ProductCreate
) -> ProductDetail:

    if db.get(Product, product_id):
        raise HTTPException(
            status_code=409,
            detail="Product with this ID already exists"
        )

    for category_id in data.categories:
        if not db.get(Category, category_id):
            raise HTTPException(
                status_code=404,
                detail=f"Category {category_id} not found"
            )


    if data.manufacturer_id is not None:
        if not db.get(Manufacturer, data.manufacturer_id):
            raise HTTPException(
                status_code=404,
                detail="Manufacturer not found"
            )

    try:
        product = Product(
            product_id=product_id,
            name=data.name,
            status=data.status,
            model=data.model,
            description=data.description,
            image=data.image,
            price=data.price,
            manufacturer_id=data.manufacturer_id,
        )

        db.add(product)
        db.flush()
        for category_id in data.categories:
            product.product_categories.append(
                ProductCategory(category_id=category_id)
            )
        for attribute in data.attributes:
            product.attributes.append(
                ProductAttribute(
                    name=attribute.name,
                    value=attribute.value
                )
            )

        for image in data.images:
            product.images.append(
                ProductImage(
                    image=image.image,
                    sort_order=image.sort_order
                )
            )

        db.commit()

        return get_product_detail(db, product_id)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Database integrity error. Check product data and foreign keys."
        )

    except Exception:
        db.rollback()
        raise

def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductDetail:
    product = get_product_or_404(db, product_id)

    changes = data.model_dump(exclude_unset=True)

    if "name" in changes and changes["name"] is None:
        raise HTTPException(422, "name cannot be null")

    if changes.get("manufacturer_id") is not None:
        if not db.get(Manufacturer, changes["manufacturer_id"]):
            raise HTTPException(404, "Manufacturer not found")

    try:
        for key, value in changes.items():
            setattr(product, key, value)

        product.date_modify = datetime.now()

        db.commit()

        return get_product_detail(db, product_id)

    except Exception:
        db.rollback()
        raise