from datetime import date
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.schemas.offers_schema import AddOfferToCart
from app.models.offer import Offer
from app.models.cart_item import CartItem
from app.models.cart import (
    Cart, 
    CartStatus,
)
from app.exceptions import (
    CartAlreadyExistsError, 
    OfferDoesNotBelongToClientError,
    CartNotFoundError,
    OfferNotFoundError,
    ExpiredOfferError,
    CartItemNotFoundError,
    CartItemDoesNotBelongToCartError,
    InvalidCartStateError,
)

class CartService:

    """
    Handles business rules related to shopping cart management.

    Responsibilities:
    - Ensure a client has only one open cart
    - Validate cart state before modifications
    - Validate offer ownership and expiration
    - Handle cart item creation and removal
    """

    def __init__(self, session: Session):

        self.session = session

    def create_cart(self, client_id: int) -> Cart:

        if self._check_existing_cart_in_progress(client_id=client_id):
            raise CartAlreadyExistsError()
        
        new_cart = Cart(client_id=client_id)
        self.session.add(new_cart)
        self.session.flush()

        return new_cart
    
    def add_offer_to_cart(self, cart_id: int, offer_to_be_added: AddOfferToCart) -> Cart:

        # Quantity validation (greater than zero) is handled at the Pydantic schema level.
        # In a production scenario, this rule could also be enforced at the service layer
        # to guarantee business rule protection beyond the API boundary

        cart, offer = self._validate_cart_and_offer(
            cart_id=cart_id,
            offer_id=offer_to_be_added.offer_id,
        )

        existing_cart_item = self._check_existing_cart_item(
            cart_id=cart.id,
            offer_id=offer.id
        )
        if existing_cart_item:

            existing_cart_item.quantity += offer_to_be_added.quantity
            return existing_cart_item.cart
        
        cart_item = CartItem(
            cart_id=cart.id,
            offer_id=offer.id,
            quantity=offer_to_be_added.quantity,
            unit_price_snapshot=offer.unit_price,
        )

        self.session.add(cart_item)
        self.session.flush()
        
        return cart_item.cart
    
    def remove_offer_from_cart(self, cart_id: int, cart_item_id: int) -> Cart:

        """
        Removes a cart item entirely from the cart.

        Note:
        In a real-world scenario, this operation could decrement the item quantity
        instead of fully removing it. However, for the scope of this technical case,
        the item is completely deleted.
        """

        cart, cart_item = self._validate_cart_and_cart_item(
            cart_id=cart_id,
            cart_item_id=cart_item_id
        )

        self.session.delete(cart_item)
        self.session.flush()

        return cart

    def _validate_cart_and_cart_item(self, cart_id: int, cart_item_id: int) -> Tuple[Cart, CartItem]:

        cart = self.validate_cart(
            cart_id=cart_id,
            require_open=True,
        )
        cart_item = self._validate_cart_item(cart_item_id=cart_item_id)

        if cart.id != cart_item.cart_id:
            raise CartItemDoesNotBelongToCartError()
        
        return cart, cart_item

    def _validate_cart_and_offer(self, cart_id: int, offer_id: int) -> Tuple[Cart, Offer]:  
            # Inventory validation is not implemented because stock control
            # is outside the scope of this technical challenge.
            
            cart = self.validate_cart(
                cart_id=cart_id,
                require_open=True,
            )
            offer = self._validate_offer(offer_id=offer_id)

            if cart.client_id != offer.client_id:
                raise OfferDoesNotBelongToClientError()
            
            return cart, offer
    
    def validate_cart(self, cart_id: int, require_open: bool = False) -> Cart:

        cart = self.session.get(Cart, cart_id)
        if not cart:
            raise CartNotFoundError(f"Cart with id {cart_id} not found.")
        
        if require_open and cart.status != CartStatus.OPEN:
            raise InvalidCartStateError(f"Cart is in '{cart.status.value}' state and cannot be modified.")
            
        return cart
    
    def _validate_offer(self, offer_id: int) -> Offer:

        offer = self.session.get(Offer, offer_id)
        if not offer:
            raise OfferNotFoundError(f"Offer with id {offer_id} not found.")
        
        if offer.valid_until < date.today():
            raise ExpiredOfferError()
        
        return offer
    
    def _validate_cart_item(self, cart_item_id: int) -> CartItem:
        
        cart_item = self.session.get(CartItem, cart_item_id)
        if not cart_item:
            raise CartItemNotFoundError()
        
        return cart_item
    
    def _check_existing_cart_item(self, cart_id: int, offer_id: int):
        
        query = (
            select(CartItem)
            .where(
                CartItem.cart_id == cart_id,
                CartItem.offer_id == offer_id
            )
        )
        return self.session.scalars(query).first()
        
    def _check_existing_cart_in_progress(self, client_id: int):

        query = (
            select(Cart)
            .where(
                Cart.client_id == client_id,
                or_(
                    Cart.status == CartStatus.OPEN,
                    Cart.status == CartStatus.CHECKOUT
                ) 
            )
        )
        return self.session.scalars(query).first()