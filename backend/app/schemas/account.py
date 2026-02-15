from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern=r"^(asset|liability)$")
    sub_type: Optional[str] = Field(None, max_length=50)
    initial_balance: Decimal = Field(default=Decimal('0'))
    credit_limit: Optional[Decimal] = Field(None, ge=0)
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None
    is_active: bool = True
    is_default: bool = False


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sub_type: Optional[str] = Field(None, max_length=50)
    credit_limit: Optional[Decimal] = Field(None, ge=0)
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class AccountResponse(AccountBase):
    id: int
    balance: Decimal
    available_balance: Decimal = Field(default=Decimal('0'))  # 可用余额（资产-负债或信用额度-已用）
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AccountSummary(BaseModel):
    """账户汇总"""
    total_assets: Decimal  # 总资产
    total_liabilities: Decimal  # 总负债
    net_worth: Decimal  # 净资产
    asset_accounts: list[AccountResponse]
    liability_accounts: list[AccountResponse]
