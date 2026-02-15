from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from typing import List, Optional
from datetime import date, timedelta
from decimal import Decimal
from app.models.transaction import Transaction, Category
from app.models.account import Account
from app.schemas.accounting import TransactionCreate, TransactionUpdate, CategoryCreate, FinanceSummary
from app.services.account_service import AccountService


class AccountingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.account_service = AccountService(db)
    
    # Category operations
    async def get_categories(
        self,
        type: Optional[str] = None
    ) -> List[Category]:
        """Get all categories"""
        query = select(Category)
        if type:
            query = query.where(Category.type == type)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create_category(self, data: CategoryCreate) -> Category:
        """Create new category"""
        category = Category(**data.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    # Transaction operations
    async def get_transactions(
        self,
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Transaction]:
        """Get transactions with filters"""
        from sqlalchemy.orm import selectinload
        
        query = select(Transaction).options(
            selectinload(Transaction.category),
            selectinload(Transaction.from_account),
            selectinload(Transaction.to_account)
        )
        
        if type:
            query = query.where(Transaction.type == type)
        if category_id:
            query = query.where(Transaction.category_id == category_id)
        if account_id:
            query = query.where(
                (Transaction.from_account_id == account_id) |
                (Transaction.to_account_id == account_id)
            )
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
        
        query = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        transactions = list(result.scalars().all())
        
        # Populate account names
        for transaction in transactions:
            if transaction.category:
                transaction.category_name = transaction.category.name
                transaction.category_icon = transaction.category.icon
                transaction.category_color = transaction.category.color
            if transaction.from_account:
                transaction.from_account_name = transaction.from_account.name
            if transaction.to_account:
                transaction.to_account_name = transaction.to_account.name
        
        return transactions
    
    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID"""
        result = await self.db.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, data: TransactionCreate) -> Transaction:
        """Create new transaction and update account balances"""
        transaction = Transaction(**data.model_dump())
        self.db.add(transaction)
        
        # 更新账户余额
        if data.type == 'income':
            # 收入：增加目标账户余额
            if data.to_account_id:
                await self.account_service.update_balance(
                    data.to_account_id,
                    data.amount,
                    'add'
                )
        elif data.type == 'expense':
            # 支出：减少源账户余额
            if data.from_account_id:
                await self.account_service.update_balance(
                    data.from_account_id,
                    data.amount,
                    'subtract'
                )
        elif data.type == 'transfer':
            # 转账：减少源账户，增加目标账户
            if data.from_account_id:
                await self.account_service.update_balance(
                    data.from_account_id,
                    data.amount,
                    'subtract'
                )
            if data.to_account_id:
                await self.account_service.update_balance(
                    data.to_account_id,
                    data.amount,
                    'add'
                )
        elif data.type == 'repayment':
            # 还款：减少源账户（资产），增加目标账户（负债，使其接近0）
            if data.from_account_id:
                await self.account_service.update_balance(
                    data.from_account_id,
                    data.amount,
                    'subtract'
                )
            if data.to_account_id:
                await self.account_service.update_balance(
                    data.to_account_id,
                    data.amount,
                    'add'
                )
        
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
    
    async def update(
        self,
        transaction_id: int,
        data: TransactionUpdate
    ) -> Optional[Transaction]:
        """Update transaction"""
        transaction = await self.get_by_id(transaction_id)
        if not transaction:
            return None
        
        # 先恢复原来的账户余额
        await self._revert_transaction_balance(transaction)
        
        # 更新交易数据
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        # 应用新的账户余额变化
        await self._apply_transaction_balance(transaction)
        
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
    
    async def delete(self, transaction_id: int) -> bool:
        """Delete transaction and revert account balances"""
        transaction = await self.get_by_id(transaction_id)
        if not transaction:
            return False
        
        # 恢复账户余额
        await self._revert_transaction_balance(transaction)
        
        await self.db.delete(transaction)
        await self.db.commit()
        return True
    
    async def _revert_transaction_balance(self, transaction: Transaction):
        """恢复交易对账户余额的影响"""
        if transaction.type == 'income':
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'subtract'
                )
        elif transaction.type == 'expense':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'add'
                )
        elif transaction.type == 'transfer':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'add'
                )
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'subtract'
                )
        elif transaction.type == 'repayment':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'add'
                )
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'subtract'
                )
    
    async def _apply_transaction_balance(self, transaction: Transaction):
        """应用交易对账户余额的影响"""
        if transaction.type == 'income':
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'add'
                )
        elif transaction.type == 'expense':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'subtract'
                )
        elif transaction.type == 'transfer':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'subtract'
                )
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'add'
                )
        elif transaction.type == 'repayment':
            if transaction.from_account_id:
                await self.account_service.update_balance(
                    transaction.from_account_id,
                    transaction.amount,
                    'subtract'
                )
            if transaction.to_account_id:
                await self.account_service.update_balance(
                    transaction.to_account_id,
                    transaction.amount,
                    'add'
                )
    
    async def get_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> FinanceSummary:
        """Get financial summary"""
        query = select(
            Transaction.type,
            func.sum(Transaction.amount)
        ).where(Transaction.type.in_(['income', 'expense']))
        
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
        
        query = query.group_by(Transaction.type)
        result = await self.db.execute(query)
        
        totals = {row[0]: row[1] for row in result.all()}
        
        total_income = totals.get('income', Decimal('0'))
        total_expense = totals.get('expense', Decimal('0'))
        
        period = "all time"
        if start_date and end_date:
            period = f"{start_date} to {end_date}"
        elif start_date:
            period = f"from {start_date}"
        elif end_date:
            period = f"until {end_date}"
        
        return FinanceSummary(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            period=period
        )
    
    async def get_monthly_summary(self, year: int, month: int) -> FinanceSummary:
        """Get monthly financial summary"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        return await self.get_summary(start_date, end_date)
