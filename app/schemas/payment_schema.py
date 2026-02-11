from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.schemas.cart_schema import CartSchema
from app.models.payment import PaymentStatus

class PaymentSchema(BaseModel):
    id: int
    cart_id: int
    status: PaymentStatus
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentResponseSchema(BaseModel):
    cart: CartSchema
    payment: PaymentSchema