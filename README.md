# E-commerce Admin API

A FastAPI-based backend API for e-commerce administration that provides detailed insights into sales, revenue, and inventory management.

## Features

### Sales Status
- Retrieve, filter, and analyze sales data
- Revenue analysis (daily, weekly, monthly, annual)
- Compare revenue across different periods
- Sales data by date range, product, and category

### Inventory Management
- View current inventory status
- Low stock alerts
- Track inventory changes over time
- Update inventory levels

## Technical Stack

- Python 3.8+
- FastAPI
- SQLAlchemy
- SQL Server
- Pydantic

## Prerequisites

- Python 3.8 or higher
- SQL Server Express or higher
- SQL Server ODBC Driver 17

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ecommerce-admin-api
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```env
SQL_SERVER=DESKTOP-OLBMVT3\SQLEXPRESS
SQL_DATABASE=ecommerce_admin
SECRET_KEY=your-secret-key-here
```

5. **Create database in SQL Server Management Studio**
```sql
CREATE DATABASE ecommerce_admin;
GO

USE ecommerce_admin;
GO

-- Create Products table
CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(1000),
    price DECIMAL(10,2) NOT NULL,
    category NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Create other tables as needed
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## API Documentation

After starting the application, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Products

```bash
# Get all products
GET /api/v1/products/

# Get single product
GET /api/v1/products/{product_id}

# Create product
POST /api/v1/products/

# Update product
PUT /api/v1/products/{product_id}

# Delete product
DELETE /api/v1/products/{product_id}
```

### Example API Usage

1. **Create a Product**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products/" \
-H "Content-Type: application/json" \
-d '{
    "name": "4K Smart TV",
    "description": "55-inch Ultra HD Smart Television",
    "price": 699.99,
    "category": "Electronics"
}'
```

2. **Get All Products**
```bash
curl "http://127.0.0.1:8000/api/v1/products/"
```

## Testing with Postman

1. **Set up environment**
   - Create new environment
   - Add variable: `base_url` = `http://127.0.0.1:8000/api/v1`

2. **Create requests**
   - Use `{{base_url}}` as prefix
   - Example: `{{base_url}}/products/`

3. **Test endpoints**
   - GET: `{{base_url}}/products/`
   - POST: `{{base_url}}/products/`
   - PUT: `{{base_url}}/products/1`
   - DELETE: `{{base_url}}/products/1`

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(1000),
    price DECIMAL(10,2) NOT NULL,
    category NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
```

## Project Structure
```
ecommerce-admin-api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── products.py
│   │   │   ├── sales.py
│   │   │   └── inventory.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── sale.py
│   │   └── inventory.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_sales.py
│   └── test_inventory.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```


