# Database Documentation

## Database Schema Overview

The e-commerce admin database consists of four main tables that manage products, inventory, sales, and inventory history. Below is a detailed explanation of each table and their relationships.

## Tables

### 1. Products Table

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

**Purpose:** Stores basic product information

- `id`: Unique identifier for each product
- `name`: Product name (required)
- `description`: Detailed product description
- `price`: Current product price
- `category`: Product category for classification
- `created_at`: Timestamp of product creation
- `updated_at`: Timestamp of last update

### 2. Inventory Table

```sql
CREATE TABLE inventory (
    id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    low_stock_threshold INT NOT NULL DEFAULT 10,
    last_updated DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Purpose:** Manages current stock levels for products

- `id`: Unique identifier for inventory record
- `product_id`: Reference to products table (one-to-one relationship)
- `quantity`: Current stock level
- `low_stock_threshold`: Minimum stock level before alert
- `last_updated`: Timestamp of last inventory update

### 3. Sales Table

```sql
CREATE TABLE sales (
    id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    sale_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Purpose:** Records all sales transactions

- `id`: Unique identifier for each sale
- `product_id`: Reference to products table
- `quantity`: Number of units sold
- `unit_price`: Price per unit at time of sale
- `total_amount`: Total transaction amount
- `sale_date`: Timestamp of the sale

### 4. Inventory History Table

```sql
CREATE TABLE inventory_history (
    id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    quantity_change INT NOT NULL,
    new_quantity INT NOT NULL,
    change_date DATETIME DEFAULT GETDATE(),
    change_type NVARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Purpose:** Tracks all inventory changes

- `id`: Unique identifier for each history record
- `product_id`: Reference to products table
- `quantity_change`: Amount changed (positive for additions, negative for reductions)
- `new_quantity`: Stock level after change
- `change_date`: Timestamp of the change
- `change_type`: Type of change (e.g., 'sale', 'restock', 'adjustment')

## Relationships

1. **Products to Inventory (One-to-One)**

   - Each product has exactly one inventory record
   - Enforced by UNIQUE constraint on `inventory.product_id`

2. **Products to Sales (One-to-Many)**

   - Each product can have multiple sales records
   - Relationship maintained through `sales.product_id`

3. **Products to Inventory History (One-to-Many)**
   - Each product can have multiple history records
   - Tracks all changes to inventory levels

## Indexes

```sql
-- Products table indexes
CREATE INDEX idx_product_category ON products(category);

-- Sales table indexes
CREATE INDEX idx_sale_date ON sales(sale_date);
CREATE INDEX idx_product_sale ON sales(product_id, sale_date);

-- Inventory History table indexes
CREATE INDEX idx_inventory_history_date ON inventory_history(change_date);
CREATE INDEX idx_product_history ON inventory_history(product_id, change_date);
```

## Common Queries

### 1. Low Stock Alert

```sql
SELECT
    p.name,
    i.quantity,
    i.low_stock_threshold
FROM products p
JOIN inventory i ON p.id = i.product_id
WHERE i.quantity <= i.low_stock_threshold;
```

### 2. Sales Analysis

```sql
-- Daily Sales Revenue
SELECT
    CONVERT(DATE, sale_date) as sale_day,
    SUM(total_amount) as daily_revenue
FROM sales
GROUP BY CONVERT(DATE, sale_date)
ORDER BY sale_day DESC;

-- Product Sales Performance
SELECT
    p.name,
    COUNT(*) as number_of_sales,
    SUM(s.quantity) as units_sold,
    SUM(s.total_amount) as total_revenue
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.name
ORDER BY total_revenue DESC;
```

### 3. Inventory Movement

```sql
SELECT
    p.name,
    ih.change_date,
    ih.quantity_change,
    ih.new_quantity,
    ih.change_type
FROM inventory_history ih
JOIN products p ON ih.product_id = p.id
ORDER BY ih.change_date DESC;
```

## Data Integrity Rules

1. **Products**

   - Product names must be unique
   - Prices must be positive
   - Categories must be from predefined list

2. **Inventory**

   - Quantity cannot be negative
   - Low stock threshold must be positive

3. **Sales**

   - Quantity must be positive
   - Unit price must match product price at time of sale
   - Total amount must equal quantity \* unit price

4. **Inventory History**
   - New quantity must reflect actual inventory level
   - Change type must be from predefined list ('sale', 'restock', 'adjustment')
