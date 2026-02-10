from typing import List
from fastapi import (
    APIRouter,
    Depends
)

from app.services.catalog_service.CatalogService import CatalogService
from app.schemas.products_schema import ProductSchema
from app.schemas.clients_schema import CustomerSchema
from app.schemas.offers_schema import OfferSchema
from app.dependencies.catalog_dependencies import get_catalog_service

catalog_router = APIRouter(prefix="/catalog")

@catalog_router.get("/products", response_model=List[ProductSchema])
def get_products(service: CatalogService = Depends(get_catalog_service)):

    return service.list_products()

@catalog_router.get("/customers", response_model=List[CustomerSchema])
def get_customers(service: CatalogService = Depends(get_catalog_service)):
    
    return service.list_customers()

@catalog_router.get("/client/offers/{client_id}", response_model=List[OfferSchema])
def collect_customer_offers(client_id: int, service: CatalogService = Depends(get_catalog_service)):
    
    return service.list_customer_offers(client_id=client_id)