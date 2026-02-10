from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.connection import get_session
from app.services.catalog_service.CatalogService import CatalogService

def get_catalog_service(session: Session = Depends(get_session)) -> CatalogService:
    return CatalogService(session=session)