from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    main_image_url: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    filter_label: Mapped[str] = mapped_column(String(80), default="", nullable=False)

    seller = relationship("Seller", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product")


class ProductVariant(Base, TimestampMixin):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    option_value_1: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    option_value_2: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    option_value_3: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    price_override: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)

    product = relationship("Product", back_populates="variants")
