from typing import List
from enum import Enum
from datetime import (
    datetime,
    timezone
)

from sqlalchemy import (
    Integer,
    ForeignKey,
    Enum as SQLEnum,
    DateTime,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class CartStatus(Enum):
    OPEN: str = "open"
    CHECKOUT: str = "checkout"
    PAID: str = "paid"


class Cart(Base):

    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    status: Mapped[CartStatus] = mapped_column(SQLEnum(CartStatus), index=True, default=CartStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")