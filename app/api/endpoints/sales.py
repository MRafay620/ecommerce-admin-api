from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.db.database import get_db
from app.db.models import Sale, Product
from app.schemas.sale import Sale as SaleSchema, SaleCreate

router = APIRouter()

@router.get("/compare-periods")
def compare_revenue_periods(
    period_1_start: datetime,
    period_1_end: datetime,
    period_2_start: datetime,
    period_2_end: datetime,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Compare revenue between two time periods."""
    def get_period_revenue(start_date, end_date):
        query = db.query(func.sum(Sale.total_amount).label('revenue'))
        if category:
            query = query.join(Product).filter(Product.category == category)
        return query.filter(
            Sale.sale_date.between(start_date, end_date)
        ).scalar() or 0
    
    period_1_revenue = get_period_revenue(period_1_start, period_1_end)
    period_2_revenue = get_period_revenue(period_2_start, period_2_end)
    
    return {
        "period_1": {
            "start": period_1_start,
            "end": period_1_end,
            "revenue": period_1_revenue
        },
        "period_2": {
            "start": period_2_start,
            "end": period_2_end,
            "revenue": period_2_revenue
        },
        "difference": period_1_revenue - period_2_revenue,
        "percentage_change": ((period_1_revenue - period_2_revenue) / period_2_revenue * 100) if period_2_revenue else 0
    }

@router.get("/revenue/breakdown")
def get_revenue_breakdown(
    start_date: datetime,
    end_date: datetime,
    group_by: str = "category",
    db: Session = Depends(get_db)
):
    """Get revenue breakdown by category or product."""
    if group_by == "category":
        query = db.query(
            Product.category,
            func.sum(Sale.total_amount).label('revenue')
        ).join(Sale)\
        .filter(Sale.sale_date.between(start_date, end_date))\
        .group_by(Product.category)
    else:
        query = db.query(
            Product.name,
            func.sum(Sale.total_amount).label('revenue')
        ).join(Sale)\
        .filter(Sale.sale_date.between(start_date, end_date))\
        .group_by(Product.name)
    
    return query.all()