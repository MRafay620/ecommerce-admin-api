from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Admin API",
    description="API for managing e-commerce sales, inventory, and analytics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.endpoints import sales, inventory, products

app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Admin API"}