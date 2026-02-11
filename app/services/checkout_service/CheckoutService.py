from typing import Tuple
from decimal import Decimal
from sqlalchemy.orm  import Session

from app.models.cart import (
    Cart,
    CartStatus
)
from app.models.payment import (
    Payment,
    PaymentStatus
)
from app.services.cart_service.CartService import CartService
from app.exceptions import (
    CartIsEmptyError,
    InvalidCartStateError,
)

class CheckoutService:

    """
    Handles the linear checkout flow for cart-to-payment transitions.

    Responsibilities:
    - Transition cart from OPEN to CHECKOUT status
    - Process payment and transition cart to PAID status
    - Calculate order totals based on cart items

    This service orchestrates a linear, happy-path flow where all validations
    are assumed to have been performed upstream. State transitions follow a
    strict sequence: OPEN -> CHECKOUT -> PAID.
    """
    
    def __init__(self, session: Session):

        self.session = session
        self.cart_service = CartService(session=session)

    def start_checkout(self, cart_id: int) -> Cart:

        cart = self.cart_service.validate_cart(
            cart_id=cart_id,
            require_open=True,
        )
        if not cart.items:
            raise CartIsEmptyError()
        
        cart.status = CartStatus.CHECKOUT
        return cart
    
    def finalize_payment(self, cart_id: int) -> Tuple[Cart, Payment]:

        cart = self.cart_service.validate_cart(cart_id=cart_id)
        if cart.status != CartStatus.CHECKOUT:
            raise InvalidCartStateError("Cannot process payment: cart is not in CHECKOUT status.")
        
        cart.status = CartStatus.PAID
        payment = Payment(
            cart_id=cart.id,
            status=PaymentStatus.PAID,
            amount=self._calculate_total(cart=cart),
        )

        self.session.add(payment)
        self.session.flush()

        return cart, payment

    def _calculate_total(self, cart: Cart) -> Decimal:
        return sum(
            map(lambda item: item.unit_price_snapshot * item.quantity, cart.items), 
            Decimal("0.00"),
        )