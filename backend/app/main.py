from fastapi import FastAPI
from app.api.v1.api import api_router
from app.config import settings

app = FastAPI(title="Marcus's Bicycle E-commerce API")

# Include the V1 API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Marcus's Bicycle E-commerce API"}

# Add startup/shutdown events later if needed for DB connection pools, etc.
# @app.on_event("startup")
# async def startup_event():
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     pass 