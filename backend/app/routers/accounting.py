from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.schemas.accounting import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    CategoryCreate, CategoryResponse, FinanceSummary
)
from app.services.accounting_service import AccountingService

router = APIRouter(prefix="/accounting", tags=["accounting"])


# Category endpoints
@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    type: Optional[str] = Query(None, regex="^(income|expense)$"),
    db: AsyncSession = Depends(get_db)
):
    """Get all categories"""
    service = AccountingService(db)
    return await service.get_categories(type=type)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new category"""
    service = AccountingService(db)
    return await service.create_category(category)


# Transaction endpoints
@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = Query(None, regex="^(income|expense|transfer|repayment)$"),
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get transactions with filters"""
    service = AccountingService(db)
    return await service.get_transactions(
        skip=skip,
        limit=limit,
        type=type,
        category_id=category_id,
        account_id=account_id,
        start_date=start_date,
        end_date=end_date
    )


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new transaction"""
    service = AccountingService(db)
    return await service.create(transaction)


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get transaction by ID"""
    service = AccountingService(db)
    transaction = await service.get_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update transaction"""
    service = AccountingService(db)
    updated = await service.update(transaction_id, transaction)
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete transaction"""
    service = AccountingService(db)
    success = await service.delete(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}


# Summary endpoints
@router.get("/summary", response_model=FinanceSummary)
async def get_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get financial summary"""
    service = AccountingService(db)
    return await service.get_summary(start_date=start_date, end_date=end_date)
