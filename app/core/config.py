from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "E-commerce Admin API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing e-commerce sales, inventory, and analytics"

# Database Configuration
    SQL_SERVER: str = os.getenv("SQL_SERVER", "DESKTOP-OLBMVT3\SQLEXPRESS")
    SQL_DATABASE: str = os.getenv("SQL_DATABASE", "ecommerce_admin")
    SQL_TRUSTED_CONNECTION: str = os.getenv("SQL_TRUSTED_CONNECTION", "yes")
    DATABASE_URL: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct Database URL for SQL Server with Windows Authentication
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"mssql+pyodbc://{self.SQL_SERVER}/{self.SQL_DATABASE}?"
                f"driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
            )

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Inventory Configuration
    DEFAULT_LOW_STOCK_THRESHOLD: int = 10
    CRITICAL_STOCK_THRESHOLD: int = 5

    # Cache Configuration
    CACHE_EXPIRATION_MINUTES: int = 10

    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct Database URL
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
                f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            )

# Create settings instance
@lru_cache()
def get_settings() -> Settings:
    """
    Get settings instance with caching using lru_cache.
    Returns:
        Settings: Application settings instance
    """
    return Settings()

# Create a settings instance for import
settings = get_settings()

# API Metadata tags for OpenAPI documentation
api_tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products, including creation and management",
    },
    {
        "name": "inventory",
        "description": "Inventory management and stock level operations",
    },
    {
        "name": "sales",
        "description": "Sales operations and analytics",
    },
]

# Error Messages
class ErrorMessages:
    PRODUCT_NOT_FOUND = "Product not found"
    INSUFFICIENT_STOCK = "Insufficient stock available"
    INVALID_QUANTITY = "Invalid quantity provided"
    DATABASE_ERROR = "Database operation failed"
    INVALID_DATE_RANGE = "Invalid date range provided"
    UNAUTHORIZED = "Not authorized to perform this action"
    VALIDATION_ERROR = "Validation error in request data"

# Constants for business logic
class BusinessConstants:
    MIN_PRICE = 0.01
    MAX_PRICE = 999999.99
    MAX_PRODUCT_NAME_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 1000
    ALLOWED_CATEGORIES = [
        "Electronics",
        "Clothing",
        "Home & Kitchen",
        "Books",
        "Toys",
        "Sports",
        "Beauty",
        "Health",
        "Automotive",
        "Others"
    ]

# Date format constants
class DateFormats:
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Response Messages
class ResponseMessages:
    SUCCESS_CREATE = "Successfully created"
    SUCCESS_UPDATE = "Successfully updated"
    SUCCESS_DELETE = "Successfully deleted"
    SUCCESS_FETCH = "Successfully retrieved"