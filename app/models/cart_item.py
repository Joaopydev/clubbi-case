from decimal import Decimal

from sqlalchemy import (
    Integer,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class CartItem(Base):

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), index=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price_snapshot: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal(0.00))
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")

    __table_args__ = (
        UniqueConstraint("cart_id", "offer_id", name="uq_cart_offer"),
    )