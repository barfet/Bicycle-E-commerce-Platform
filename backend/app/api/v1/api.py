from fastapi import APIRouter

# Import individual routers here later
# from .endpoints import items, users

api_router = APIRouter()

# Include routers here later
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])

@api_router.get("/health", status_code=200)
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"} 