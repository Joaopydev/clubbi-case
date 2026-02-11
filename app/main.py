from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import BusinessException

from app.routers.cart_router import cart_router
from app.routers.catalog_router import catalog_router
from app.routers.checkout_router import checkout_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação"""
    # Startup
    from app.db.connection import get_engine
    from app.db.base import Base
    import app.models.cart
    import app.models.product
    import app.models.cart_item
    import app.models.payment
    import app.models.offer
    import app.models.client


    
    print("🚀 Iniciando Clubbi E-commerce API...")
    
    # Criar tabelas
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas do banco criadas/verificadas")
    
    print("📚 Documentação disponível em: http://localhost:8000/docs")
    print("-" * 50)
    
    yield
    
    # Shutdown
    print("-" * 50)
    print("👋 Encerrando Clubbi E-commerce API...")


app = FastAPI(
    title="Clubbi API E-commerce",
    description="API for B2B shopping cart management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


#Include routers
app.include_router(cart_router, prefix="/api/v1", tags=["Cart"])
app.include_router(catalog_router, prefix="/api/v1", tags=["Catalog"])
app.include_router(checkout_router, prefix="/api/v1", tags=["Checkout"])


@app.exception_handler(BusinessException)
def business_exception_handler(_: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.detail,
        },
    )


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Clubbi E-commerce API",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}