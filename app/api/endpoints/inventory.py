from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models import Inventory, InventoryHistory, Product
from app.schemas.inventory import (
    Inventory as InventorySchema,
    InventoryUpdate,
    InventoryHistory as InventoryHistorySchema
)

router = APIRouter()

@router.get("/low-stock", response_model=List[InventorySchema])
def get_low_stock_items(db: Session = Depends(get_db)):
    """Get items where current quantity is below the low stock threshold."""
    return db.query(Inventory).filter(
        Inventory.quantity <= Inventory.low_stock_threshold
    ).all()

@router.get("/status/{product_id}", response_model=InventorySchema)
def get_inventory_status(product_id: int, db: Session = Depends(get_db)):
    """Get current inventory status for a specific product."""
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory

@router.put("/{product_id}", response_model=InventorySchema)
def update_inventory(
    product_id: int,
    update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    """Update inventory levels and threshold."""
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if update.quantity is not None:
        quantity_change = update.quantity - inventory.quantity
        inventory_history = InventoryHistory(
            product_id=product_id,
            quantity_change=quantity_change,
            new_quantity=update.quantity,
            change_type='adjustment'
        )
        db.add(inventory_history)
        inventory.quantity = update.quantity
    
    if update.low_stock_threshold is not None:
        inventory.low_stock_threshold = update.low_stock_threshold
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/history/{product_id}", response_model=List[InventoryHistorySchema])
def get_inventory_history(
    product_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get inventory change history for a specific product."""
    return db.query(InventoryHistory)\
        .filter(InventoryHistory.product_id == product_id)\
        .order_by(InventoryHistory.change_date.desc())\
        .limit(limit)\
        .all()