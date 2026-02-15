from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from decimal import Decimal
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.account import AccountCreate, AccountUpdate, AccountSummary, AccountResponse


class AccountService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self,
        type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Account]:
        """获取所有账户"""
        query = select(Account)
        
        if type:
            query = query.where(Account.type == type)
        if is_active is not None:
            query = query.where(Account.is_active == is_active)
        
        query = query.order_by(Account.is_default.desc(), Account.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, account_id: int) -> Optional[Account]:
        """根据ID获取账户"""
        result = await self.db.execute(
            select(Account).where(Account.id == account_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, data: AccountCreate) -> Account:
        """创建账户"""
        # 如果设置为默认账户，取消其他默认账户
        if data.is_default:
            await self._clear_default_accounts(data.type)
        
        account = Account(**data.model_dump())
        account.balance = data.initial_balance
        
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def update(self, account_id: int, data: AccountUpdate) -> Optional[Account]:
        """更新账户"""
        account = await self.get_by_id(account_id)
        if not account:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        # 如果设置为默认账户，取消其他默认账户
        if update_data.get('is_default'):
            await self._clear_default_accounts(account.type)
        
        for field, value in update_data.items():
            setattr(account, field, value)
        
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def delete(self, account_id: int) -> bool:
        """删除账户"""
        account = await self.get_by_id(account_id)
        if not account:
            return False
        
        # 检查是否有关联交易
        result = await self.db.execute(
            select(func.count(Transaction.id)).where(
                (Transaction.from_account_id == account_id) |
                (Transaction.to_account_id == account_id)
            )
        )
        transaction_count = result.scalar()
        
        if transaction_count > 0:
            # 如果有交易记录，只标记为不活跃
            account.is_active = False
            await self.db.commit()
        else:
            # 如果没有交易记录，可以删除
            await self.db.delete(account)
            await self.db.commit()
        
        return True
    
    async def update_balance(
        self,
        account_id: int,
        amount: Decimal,
        operation: str = 'add'
    ) -> Optional[Account]:
        """更新账户余额"""
        account = await self.get_by_id(account_id)
        if not account:
            return None
        
        if operation == 'add':
            account.balance += amount
        elif operation == 'subtract':
            account.balance -= amount
        else:
            raise ValueError(f"Invalid operation: {operation}")
        
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def get_summary(self) -> AccountSummary:
        """获取账户汇总"""
        # 获取所有活跃账户
        accounts = await self.get_all(is_active=True)
        
        asset_accounts = []
        liability_accounts = []
        total_assets = Decimal('0')
        total_liabilities = Decimal('0')
        
        for account in accounts:
            # 计算可用余额
            if account.type == 'asset':
                available_balance = account.balance
                total_assets += account.balance
                asset_accounts.append(self._to_response(account, available_balance))
            else:  # liability
                # 负债账户：余额为负数表示欠款
                if account.credit_limit:
                    # 信用卡：可用额度 = 信用额度 + 余额（余额为负）
                    available_balance = account.credit_limit + account.balance
                else:
                    # 普通负债：可用余额就是余额
                    available_balance = account.balance
                
                total_liabilities += abs(account.balance)
                liability_accounts.append(self._to_response(account, available_balance))
        
        return AccountSummary(
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            net_worth=total_assets - total_liabilities,
            asset_accounts=asset_accounts,
            liability_accounts=liability_accounts
        )
    
    async def _clear_default_accounts(self, account_type: str):
        """清除同类型的默认账户标记"""
        result = await self.db.execute(
            select(Account).where(
                and_(
                    Account.type == account_type,
                    Account.is_default == True
                )
            )
        )
        accounts = result.scalars().all()
        for account in accounts:
            account.is_default = False
        await self.db.commit()
    
    def _to_response(self, account: Account, available_balance: Decimal) -> AccountResponse:
        """转换为响应模型"""
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
