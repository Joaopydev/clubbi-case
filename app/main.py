from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.cart_exceptions import BusinessException

app = FastAPI(
    title="Clubbi API E-commerce",
    description="API for B2B shopping cart management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

from app.routers.carts_router import cart_router
from app.routers.catalog_router import catalog_router
from app.routers.orders_router import order_router

#Include routers
app.include_router(cart_router, prefix="/api/v1", tags=["Cart"])
app.include_router(catalog_router, prefix="/api/v1", tags=["Catalog"])
app.include_router(order_router, prefix="/api/v1", tags=["Orders"])

@app.exception_handler(BusinessException)
async def business_exception_handler(_: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Clubbi E-commerce API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}