from pydantic import BaseModel


class ProductCreateRequest(BaseModel):
    seller_id: int
    title: str
    base_price: float
    description: str = ""
    main_image_url: str = ""
    filter_label: str = ""


class AdminOrderStatusUpdateRequest(BaseModel):
    payment_status: str | None = None
    fulfillment_status: str | None = None


class AdminOrderStatusUpdateResponse(BaseModel):
    order_id: int
    payment_status: str
    fulfillment_status: str
