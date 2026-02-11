from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.connection import get_session
from app.services.checkout_service.CheckoutService import CheckoutService


def get_checkout_service(session: Session = Depends(get_session)) -> CheckoutService:
    return CheckoutService(session=session)