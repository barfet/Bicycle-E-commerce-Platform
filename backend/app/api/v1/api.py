from fastapi import APIRouter

# Import individual routers here later
# from .endpoints import items, users
from .endpoints import auth
from .endpoints import product_types

api_router = APIRouter()

# Include routers here later
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(product_types.router, prefix="/admin", tags=["Admin - Product Types"])

@api_router.get("/health", status_code=200)
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"} 