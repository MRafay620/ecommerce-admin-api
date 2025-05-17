from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    low_stock_threshold: Optional[int] = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None

class Inventory(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class InventoryHistoryBase(BaseModel):
    product_id: int
    quantity_change: int
    new_quantity: int
    change_type: str

class InventoryHistory(InventoryHistoryBase):
    id: int
    change_date: datetime

    class Config:
        orm_mode = True