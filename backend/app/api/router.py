from fastapi import APIRouter

from app.api import admin, auth, buyer, orders

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(buyer.router)
api_router.include_router(orders.router)
api_router.include_router(admin.router)
