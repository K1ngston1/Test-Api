from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models import Product
from services.product import get_product_or_404


def product_dep(product_id: int, db: Session = Depends(get_db)) -> Product:
    return get_product_or_404(db, product_id)
