from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.models.cart import CartStatus
from app.schemas.cart_items_schema import CartItemSchema

class CartSchema(BaseModel):
    id: int
    client_id: int
    status: CartStatus
    created_at: datetime
    items: List[CartItemSchema] = []

    class Config:
        from_attributes = True