from fastapi import (
    APIRouter,
    Depends,
)

from app.services.checkout_service.CheckoutService import CheckoutService
from app.schemas.cart_schema import CartSchema
from app.schemas.payment_schema import PaymentResponseSchema
from app.dependencies.checkout_dependencies import get_checkout_service


checkout_router = APIRouter(prefix="/checkout")

@checkout_router.post("/{cart_id}", response_model=CartSchema)
def checkout(cart_id: int, service: CheckoutService = Depends(get_checkout_service)):

    return service.start_checkout(cart_id=cart_id)


@checkout_router.post("/payment/{cart_id}", response_model=PaymentResponseSchema)
def payment(cart_id: int, service: CheckoutService = Depends(get_checkout_service)):

    cart, payment = service.finalize_payment(cart_id=cart_id)
    return {"cart": cart, "payment": payment}