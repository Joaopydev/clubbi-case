from datetime import date
from decimal import Decimal
from pydantic import (
    BaseModel,
    Field,
)


class OfferSchema(BaseModel):
    id: int
    client_id: int
    product_id: int
    unit_price: Decimal
    valid_until: date

    class Config:
        from_attributes = True


class AddOfferToCart(BaseModel):
    offer_id: int
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")
