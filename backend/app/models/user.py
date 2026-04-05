from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    line_user_id: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="buyer", nullable=False)

    seller = relationship("Seller", back_populates="owner", uselist=False)
