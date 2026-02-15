from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.schemas.account import (
    AccountCreate, AccountUpdate, AccountResponse, AccountSummary
)
from app.services.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[AccountResponse])
async def get_accounts(
    type: Optional[str] = Query(None, regex="^(asset|liability)$"),
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取所有账户"""
    service = AccountService(db)
    accounts = await service.get_all(type=type, is_active=is_active)
    
    # 转换为响应模型
    result = []
    for account in accounts:
        if account.type == 'asset':
            available_balance = account.balance
        else:  # liability
            if account.credit_limit:
                available_balance = account.credit_limit + account.balance
            else:
                available_balance = account.balance
        
        result.append(AccountResponse(
            id=account.id,
            name=account.name,
            type=account.type,
            sub_type=account.sub_type,
            balance=account.balance,
            initial_balance=account.initial_balance,
            credit_limit=account.credit_limit,
            icon=account.icon,
            color=account.color,
            description=account.description,
            is_active=account.is_active,
            is_default=account.is_default,
            available_balance=available_balance,
            created_at=account.created_at,
            updated_at=account.updated_at
        ))
    
    return result


@router.get("/summary", response_model=AccountSummary)
async def get_account_summary(db: AsyncSession = Depends(get_db)):
    """获取账户汇总"""
    service = AccountService(db)
    return await service.get_summary()


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取账户详情"""
    service = AccountService(db)
    account = await service.get_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 计算可用余额
    if account.type == 'asset':
        available_balance = account.balance
    else:  # liability
        if account.credit_limit:
            available_balance = account.credit_limit + account.balance
        else:
            available_balance = account.balance
    
    return AccountResponse(
        id=account.id,
        name=account.name,
        type=account.type,
        sub_type=account.sub_type,
        balance=account.balance,
        initial_balance=account.initial_balance,
        credit_limit=account.credit_limit,
        icon=account.icon,
        color=account.color,
        description=account.description,
        is_active=account.is_active,
        is_default=account.is_default,
        available_balance=available_balance,
        created_at=account.created_at,
        updated_at=account.updated_at
    )


@router.post("", response_model=AccountResponse, status_code=201)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建账户"""
    service = AccountService(db)
    created = await service.create(account)
    
    # 计算可用余额
    if created.type == 'asset':
        available_balance = created.balance
    else:  # liability
        if created.credit_limit:
            available_balance = created.credit_limit + created.balance
        else:
            available_balance = created.balance
    
    return AccountResponse(
        id=created.id,
        name=created.name,
        type=created.type,
        sub_type=created.sub_type,
        balance=created.balance,
        initial_balance=created.initial_balance,
        credit_limit=created.credit_limit,
        icon=created.icon,
        color=created.color,
        description=created.description,
        is_active=created.is_active,
        is_default=created.is_default,
        available_balance=available_balance,
        created_at=created.created_at,
        updated_at=created.updated_at
    )


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account: AccountUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新账户"""
    service = AccountService(db)
    updated = await service.update(account_id, account)
    if not updated:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 计算可用余额
    if updated.type == 'asset':
        available_balance = updated.balance
    else:  # liability
        if updated.credit_limit:
            available_balance = updated.credit_limit + updated.balance
        else:
            available_balance = updated.balance
    
    return AccountResponse(
        id=updated.id,
        name=updated.name,
        type=updated.type,
        sub_type=updated.sub_type,
        balance=updated.balance,
        initial_balance=updated.initial_balance,
        credit_limit=updated.credit_limit,
        icon=updated.icon,
        color=updated.color,
        description=updated.description,
        is_active=updated.is_active,
        is_default=updated.is_default,
        available_balance=available_balance,
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )


@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除账户"""
    service = AccountService(db)
    success = await service.delete(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted or deactivated successfully"}
