from enum import Enum
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, Enum as SQLEnum, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PaymentStatus(Enum):
    OPEN: str = "open"
    CHECKOUT: str = "checkout"
    PAID: str = "paid"


class Cart(Base):

    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.OPEN)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal(0.00))
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))