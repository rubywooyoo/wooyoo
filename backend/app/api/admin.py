from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.order import Order
from app.models.product import Product
from app.schemas.admin import (
    AdminOrderStatusUpdateRequest,
    AdminOrderStatusUpdateResponse,
    ProductCreateRequest,
)
from app.services.line_service import enqueue_order_status_push

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/products")
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)):
    product = Product(
        seller_id=payload.seller_id,
        title=payload.title,
        description=payload.description,
        base_price=payload.base_price,
        main_image_url=payload.main_image_url,
        filter_label=payload.filter_label,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"id": product.id, "title": product.title, "base_price": product.base_price}


@router.patch("/orders/{order_id}/status", response_model=AdminOrderStatusUpdateResponse)
def update_order_status(
    order_id: int,
    payload: AdminOrderStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> AdminOrderStatusUpdateResponse:
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.payment_status is not None:
        order.payment_status = payload.payment_status
    if payload.fulfillment_status is not None:
        order.fulfillment_status = payload.fulfillment_status
    db.add(order)
    db.commit()
    db.refresh(order)
    enqueue_order_status_push(order.id)
    return AdminOrderStatusUpdateResponse(
        order_id=order.id,
        payment_status=order.payment_status,
        fulfillment_status=order.fulfillment_status,
    )
