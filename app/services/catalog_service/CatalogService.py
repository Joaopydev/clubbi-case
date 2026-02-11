from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.client import Client
from app.models.offer import Offer

class CatalogService:

    """
    Handles read-only operations related to catalog data.

    Responsibilities:
    - List available products
    - List registered customers
    - Retrieve offers available for a specific client

    This service does not modify data and contains no business state transitions.
    """
    
    def __init__(self, session: Session):

        self.session = session

    def list_products(self) -> List[Product]:

        query = select(Product)
        return self.session.scalars(query).all()
    
    def list_customers(self) -> List[Client]:

        query = select(Client)
        return self.session.scalars(query).all()
    
    def list_customer_offers(
        self,
        client_id: int
    ) -> List[Offer]:
        
        query = select(Offer).where(Offer.client_id == client_id)
        return self.session.scalars(query).all()