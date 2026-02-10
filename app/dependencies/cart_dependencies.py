from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.connection import get_session
from app.services.cart_service.CartService import CartService


def get_cart_service(session: Session = Depends(get_session)) -> CartService:
    return CartService(session=session)