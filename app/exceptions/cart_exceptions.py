class BusinessException(Exception):
    status_code: int = 400
    detail: str = "Business rule error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)
            

class CartAlreadyExistsError(BusinessException):
    status_code = 400
    detail = "Customer already has an open shopping cart."


class OfferDoesNotBelongToClientError(BusinessException):
    status_code = 400
    detail = "The offer does not belong to the customer of this cart."


class CartNotFound(BusinessException):
    status_code = 404
    detail = "Cart not found."


class OfferNotFound(BusinessException):
    status_code = 404
    detail = "Offer not found."


class ExpiredOfferError(BusinessException):
    status_code = 400
    detail = "The offer has expired."


class CartItemNotFound(BusinessException):
    status_code = 400
    detail = "The item in the cart does not exist."
    

class CartItemDoesNotBelongToCartError(BusinessException):
    status_code = 400
    detail = "The specified item does not belong to this cart."
    

class InvalidCartStateError(BusinessException):
    status_code = 400
    detail = "The cart cannot be modified in its current state."