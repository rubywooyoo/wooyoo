from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.common import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_no: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    buyer_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"), nullable=False, index=True)
    subtotal_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    shipping_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), default="unpaid", nullable=False)
    fulfillment_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default="card", nullable=False)
    shipping_method: Mapped[str] = mapped_column(String(30), default="home_delivery", nullable=False)
    receiver_name: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    receiver_phone: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    receiver_address: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    remark: Mapped[str] = mapped_column(Text, default="", nullable=False)


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("product_variants.id"), nullable=False, index=True)
    product_title_snapshot: Mapped[str] = mapped_column(String(200), nullable=False)
    variant_snapshot: Mapped[str] = mapped_column(String(200), default="", nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal_amount: Mapped[float] = mapped_column(Float, nullable=False)
