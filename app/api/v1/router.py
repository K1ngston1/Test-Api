from fastapi import APIRouter

from api.v1.endpoints import attribute, category, image, product, store

api_router = APIRouter()
for module in (product, image, category, attribute, store):
    api_router.include_router(module.router)
