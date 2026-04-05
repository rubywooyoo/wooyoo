from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["orders"])


class CheckoutRequest(BaseModel):
    buyer_user_id: int
    seller_id: int
    total_amount: float
    payment_method: str = "card"


class CheckoutResponse(BaseModel):
    order_no: str
    payment_url: str
    created_at: datetime


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(payload: CheckoutRequest) -> CheckoutResponse:
    order_no = f"SB{uuid4().hex[:12].upper()}"
    return CheckoutResponse(
        order_no=order_no,
        payment_url=f"https://pay.example.com/{order_no}?method={payload.payment_method}",
        created_at=datetime.utcnow(),
    )
