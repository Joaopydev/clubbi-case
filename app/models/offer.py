from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Numeric, Date

from app.db.base import Base


class Offer(Base):

    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal(0.00))
    valid_until: Mapped[date] = mapped_column(Date, index=True)