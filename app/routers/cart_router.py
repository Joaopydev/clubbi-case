from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.dependencies.cart_dependencies import get_cart_service
from app.services.cart_service.CartService import CartService
from app.schemas.carts_schema import CartSchema
from app.schemas.offers_schema import AddOfferToCart
from app.schemas.cart_items_schema import (
    CartItemSchema,
)

cart_router = APIRouter(prefix="/cart")

@cart_router.post("/create-cart/{client_id}", status_code=status.HTTP_201_CREATED, response_model=CartSchema)
def create_cart(client_id: int, service: CartService = Depends(get_cart_service)):

    return service.create_cart(client_id=client_id)
    
@cart_router.post("/{cart_id}/items", response_model=CartItemSchema)
def add_offer(cart_id: int, offer: AddOfferToCart, service: CartService = Depends(get_cart_service)):
    
    return service.add_offer_to_cart(
        cart_id=cart_id,
        offer_to_be_added=offer,
    )


@cart_router.delete("/{cart_id}/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_offer(cart_id: int, cart_item_id: int, service: CartService = Depends(get_cart_service)):

    service.remove_offer_from_cart(
        cart_id=cart_id,
        cart_item_id=cart_item_id
    )