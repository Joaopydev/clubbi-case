from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class OfferSchema(BaseModel):
    id: int
    client_id: int
    product_id: int
    unit_price: Decimal
    valid_until: date

    class Config:
        from_attribute = True
