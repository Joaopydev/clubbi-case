from datetime import datetime
from pydantic import BaseModel

from app.models.cart import CartStatus

class CartSchema(BaseModel):
    id: int
    client_id: int
    status: CartStatus
    created_at: datetime

    class Config:
        from_attributes = True