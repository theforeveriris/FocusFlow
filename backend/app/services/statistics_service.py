from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date, extract, case
from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from decimal import Decimal
from app.models.timer import TimerSession
from app.models.plan import Plan
from app.models.project import Project
from app.models.transaction import Transaction, Category
from app.models.account import Account


class StatisticsService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _get_date_range(self, start_date: Optional[date], end_date: Optional[date]):
        """Get default date range if not provided"""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = date(end_date.year, end_date.month, 1)
        return start_date, end_date
    
    async def get_overview(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get overview statistics"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        # Timer stats
        timer_query = select(
            func.sum(TimerSession.duration).label('total_duration'),
            func.count(TimerSession.id).label('session_count'),
            func.avg(TimerSession.focus_score).label('avg_focus_score')
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None)
        )
        
        timer_result = await self.db.execute(timer_query)
        timer_row = timer_result.first()
        
        # Plan stats
        plan_query = select(
            func.count(Plan.id).label('total_plans'),
            func.sum(
                case((Plan.status == 'completed', 1), else_=0)
            ).label('completed_plans')
        ).where(
            cast(Plan.created_at, Date) >= start_date,
            cast(Plan.created_at, Date) <= end_date
        )
        
        plan_result = await self.db.execute(plan_query)
        plan_row = plan_result.first()
        
        # Finance stats
        income_query = select(
            func.sum(Transaction.amount)
        ).where(
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        )
        
        expense_query = select(
            func.sum(Transaction.amount)
        ).where(
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        )
        
        income_result = await self.db.execute(income_query)
        expense_result = await self.db.execute(expense_query)
        
        total_income = income_result.scalar() or 0
        total_expense = expense_result.scalar() or 0
        
        # Net worth (current)
        asset_query = select(func.sum(Account.balance)).where(Account.type == 'asset')
        liability_query = select(func.sum(Account.balance)).where(Account.type == 'liability')
        
        asset_result = await self.db.execute(asset_query)
        liability_result = await self.db.execute(liability_query)
        
        total_assets = asset_result.scalar() or 0
        total_liabilities = abs(liability_result.scalar() or 0)
        
        return {
            'total_duration': int(timer_row.total_duration or 0),
            'session_count': int(timer_row.session_count or 0),
            'avg_focus_score': float(timer_row.avg_focus_score or 0),
            'completed_plans': int(plan_row.completed_plans or 0),
            'total_plans': int(plan_row.total_plans or 0),
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net_worth': float(total_assets - total_liabilities)
        }
    
    async def get_time_trend(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get time trend data"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        # Generate date range
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        
        # Get timer data
        timer_query = select(
            cast(TimerSession.start_time, Date).label('date'),
            func.sum(TimerSession.duration).label('duration')
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None)
        ).group_by(cast(TimerSession.start_time, Date))
        
        timer_result = await self.db.execute(timer_query)
        timer_data = {row.date: row.duration for row in timer_result.all()}
        
        # Get plan completion data
        plan_query = select(
            cast(Plan.updated_at, Date).label('date'),
            func.count(Plan.id).label('completed')
        ).where(
            Plan.status == 'completed',
            cast(Plan.updated_at, Date) >= start_date,
            cast(Plan.updated_at, Date) <= end_date
        ).group_by(cast(Plan.updated_at, Date))
        
        plan_result = await self.db.execute(plan_query)
        plan_data = {row.date: row.completed for row in plan_result.all()}
        
        return [
            {
                'date': str(d),
                'duration': timer_data.get(d, 0),
                'completed_plans': plan_data.get(d, 0)
            }
            for d in dates
        ]
    
    async def get_plan_completion(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get plan completion statistics"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            Plan.status,
            func.count(Plan.id).label('count')
        ).where(
            cast(Plan.created_at, Date) >= start_date,
            cast(Plan.created_at, Date) <= end_date
        ).group_by(Plan.status)
        
        result = await self.db.execute(query)
        data = result.all()
        
        status_names = {
            'todo': '待办',
            'in_progress': '进行中',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        
        return [
            {
                'name': status_names.get(row.status, row.status),
                'value': row.count
            }
            for row in data
        ]
    
    async def get_project_time(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get project time distribution"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            Project.id,
            Project.name,
            Project.color,
            func.sum(TimerSession.duration).label('duration')
        ).join(
            TimerSession,
            Project.id == TimerSession.project_id
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None)
        ).group_by(
            Project.id
        ).order_by(
            func.sum(TimerSession.duration).desc()
        ).limit(10)
        
        result = await self.db.execute(query)
        
        return [
            {
                'name': row.name,
                'duration': row.duration or 0,
                'color': row.color
            }
            for row in result.all()
        ]
    
    async def get_focus_trend(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get focus score trend"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            cast(TimerSession.start_time, Date).label('date'),
            func.avg(TimerSession.focus_score).label('focus_score')
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None),
            TimerSession.focus_score.isnot(None)
        ).group_by(
            cast(TimerSession.start_time, Date)
        ).order_by(
            cast(TimerSession.start_time, Date)
        )
        
        result = await self.db.execute(query)
        
        return [
            {
                'date': str(row.date),
                'focus_score': round(float(row.focus_score), 1)
            }
            for row in result.all()
        ]
    
    async def get_heatmap(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get time heatmap data"""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = date(end_date.year, 1, 1)
        
        query = select(
            cast(TimerSession.start_time, Date).label('date'),
            func.sum(TimerSession.duration).label('duration')
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None)
        ).group_by(
            cast(TimerSession.start_time, Date)
        )
        
        result = await self.db.execute(query)
        
        return [
            {
                'date': str(row.date),
                'duration': row.duration
            }
            for row in result.all()
        ]
    
    async def get_finance_trend(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get finance trend data"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        # Generate date range
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        
        # Get income data
        income_query = select(
            Transaction.transaction_date,
            func.sum(Transaction.amount).label('amount')
        ).where(
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(Transaction.transaction_date)
        
        income_result = await self.db.execute(income_query)
        income_data = {row.transaction_date: float(row.amount) for row in income_result.all()}
        
        # Get expense data
        expense_query = select(
            Transaction.transaction_date,
            func.sum(Transaction.amount).label('amount')
        ).where(
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(Transaction.transaction_date)
        
        expense_result = await self.db.execute(expense_query)
        expense_data = {row.transaction_date: float(row.amount) for row in expense_result.all()}
        
        return [
            {
                'date': str(d),
                'income': income_data.get(d, 0),
                'expense': expense_data.get(d, 0)
            }
            for d in dates
        ]
    
    async def get_expense_category(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get expense category distribution"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            Category.name,
            Category.color,
            func.sum(Transaction.amount).label('amount')
        ).join(
            Transaction,
            Category.id == Transaction.category_id
        ).where(
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(
            Category.id
        ).order_by(
            func.sum(Transaction.amount).desc()
        )
        
        result = await self.db.execute(query)
        
        return [
            {
                'name': row.name,
                'value': float(row.amount),
                'itemStyle': {'color': row.color}
            }
            for row in result.all()
        ]
    
    async def get_daily_distribution(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[float]:
        """Get daily time distribution (by weekday)"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            extract('dow', TimerSession.start_time).label('weekday'),
            func.sum(TimerSession.duration).label('duration')
        ).where(
            cast(TimerSession.start_time, Date) >= start_date,
            cast(TimerSession.start_time, Date) <= end_date,
            TimerSession.end_time.isnot(None)
        ).group_by(
            extract('dow', TimerSession.start_time)
        )
        
        result = await self.db.execute(query)
        data = {int(row.weekday): row.duration for row in result.all()}
        
        # Convert to Monday-Sunday (0-6)
        # PostgreSQL dow: 0=Sunday, 1=Monday, ..., 6=Saturday
        # We want: 0=Monday, 1=Tuesday, ..., 6=Sunday
        weekday_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 0: 6}
        
        result_data = [0.0] * 7
        for pg_dow, duration in data.items():
            our_dow = weekday_map.get(pg_dow, 0)
            result_data[our_dow] = round(duration / 3600, 1)
        
        return result_data
    
    async def get_priority_distribution(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[float]:
        """Get plan priority distribution"""
        start_date, end_date = self._get_date_range(start_date, end_date)
        
        query = select(
            Plan.priority_matrix,
            func.count(Plan.id).label('count')
        ).where(
            cast(Plan.created_at, Date) >= start_date,
            cast(Plan.created_at, Date) <= end_date
        ).group_by(
            Plan.priority_matrix
        )
        
        result = await self.db.execute(query)
        data = {row.priority_matrix: row.count for row in result.all()}
        
        total = sum(data.values()) or 1
        
        # Return in order: urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important
        priorities = [
            'urgent_important',
            'not_urgent_important',
            'urgent_not_important',
            'not_urgent_not_important'
        ]
        
        return [
            round((data.get(p, 0) / total) * 100, 1)
            for p in priorities
        ]
