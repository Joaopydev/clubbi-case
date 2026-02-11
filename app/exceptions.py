"""
Business exceptions for Clubbi E-commerce API.

All business rule violations should raise these exceptions
instead of generic HTTPException.
"""


# BASE EXCEPTION

class BusinessException(Exception):
    """Base exception for all business rule violations"""
    status_code: int = 400
    detail: str = "Business rule error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


# CART EXCEPTIONS

class CartAlreadyExistsError(BusinessException):
    """Raised when client tries to create a second open cart"""
    status_code = 400
    detail = "Customer already has an open shopping cart."


class CartNotFoundError(BusinessException):
    """Raised when cart ID doesn't exist"""
    status_code = 404
    detail = "Cart not found."


class CartIsEmptyError(BusinessException):
    """Raised when trying to checkout an empty cart"""
    status_code = 400
    detail = "It is not possible to proceed with an empty cart."


class InvalidCartStateError(BusinessException):
    """Raised when trying to modify a non-open cart"""
    status_code = 400
    detail = "The cart cannot be modified in its current state."


# CART ITEM EXCEPTIONS

class CartItemNotFoundError(BusinessException):
    """Raised when cart item ID doesn't exist"""
    status_code = 404
    detail = "The item in the cart does not exist."


class CartItemDoesNotBelongToCartError(BusinessException):
    """Raised when item doesn't belong to the specified cart"""
    status_code = 403
    detail = "The specified item does not belong to this cart."


# OFFER EXCEPTIONS

class OfferNotFoundError(BusinessException):
    """Raised when offer ID doesn't exist"""
    status_code = 404
    detail = "Offer not found."


class OfferDoesNotBelongToClientError(BusinessException):
    """Raised when offer doesn't belong to cart's client"""
    status_code = 403
    detail = "The offer does not belong to the customer of this cart."


class ExpiredOfferError(BusinessException):
    """Raised when trying to use an expired offer"""
    status_code = 400
    detail = "The offer has expired."