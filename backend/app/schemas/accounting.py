from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern=r"^(income|expense)$")
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    parent_id: Optional[int] = None
    budget_limit: Optional[Decimal] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    type: str = Field(..., pattern=r"^(income|expense|transfer|repayment)$")
    amount: Decimal = Field(..., gt=0)
    category_id: Optional[int] = None
    from_account_id: Optional[int] = None  # 转出账户（支出、转账、还款）
    to_account_id: Optional[int] = None  # 转入账户（收入、转账）
    plan_id: Optional[int] = None
    project_id: Optional[int] = None
    transaction_date: date
    description: Optional[str] = None
    tags: List[str] = []


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: Optional[str] = Field(None, pattern=r"^(income|expense|transfer|repayment)$")
    amount: Optional[Decimal] = Field(None, gt=0)
    category_id: Optional[int] = None
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    plan_id: Optional[int] = None
    project_id: Optional[int] = None
    transaction_date: Optional[date] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    category_color: Optional[str] = None
    from_account_name: Optional[str] = None
    to_account_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class FinanceSummary(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    period: str
