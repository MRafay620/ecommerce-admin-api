from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales = relationship("Sale", back_populates="product")
    
    # Indexes
    __table_args__ = (
        Index('idx_product_category', 'category'),
    )

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True)
    quantity = Column(Integer, nullable=False, default=0)
    low_stock_threshold = Column(Integer, nullable=False, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory")

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="sales")
    
    # Indexes
    __table_args__ = (
        Index('idx_sale_date', 'sale_date'),
        Index('idx_product_sale', 'product_id', 'sale_date'),
    )

class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity_change = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    change_date = Column(DateTime, default=datetime.utcnow)
    change_type = Column(String(50))  # 'restock', 'sale', 'adjustment'
    
    # Indexes
    __table_args__ = (
        Index('idx_inventory_history_date', 'change_date'),
        Index('idx_product_history', 'product_id', 'change_date'),
    )