from decimal import Decimal
from pydantic import BaseModel


class CartItemSchema(BaseModel):
    id: int
    cart_id: int
    offer_id: int
    quantity: int
    unit_price_snapshot: Decimal

    class Config:
        from_attributes = True

class CartItemToBeDeleted(BaseModel):
    id: int