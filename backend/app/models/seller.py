from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import TimestampMixin


class Seller(Base, TimestampMixin):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    announcement: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    logo_url: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    cover_url: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner = relationship("User", back_populates="seller")
    campaigns = relationship("Campaign", back_populates="seller")
    products = relationship("Product", back_populates="seller")
