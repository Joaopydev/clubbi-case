from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.catalog_service.CatalogService import CatalogService
from app.schemas.products_schema import ProductSchema
from app.schemas.clients_schema import CustomerSchema
from app.schemas.offers_schema import OfferSchema
from app.db.connection import get_session

catalog_router = APIRouter(prefix="/catalog")

@catalog_router.get("/products", response_model=List[ProductSchema])
def get_products(session: Session = Depends(get_session)):

    service = CatalogService(session=session)
    return service.list_products()

@catalog_router.get("/customers", response_model=List[CustomerSchema])
def get_customers(session: Session = Depends(get_session)):
    
    service = CatalogService(session=session)
    return service.list_customers()

@catalog_router.get("/client/offers/{client_id}", response_model=List[OfferSchema])
def collect_customer_offers(client_id: int, session: Session = Depends(get_session)):
    
    service = CatalogService(session=session)
    return service.list_customer_offers(client_id=client_id)