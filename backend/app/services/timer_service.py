from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract, cast, Date
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from app.models.timer import TimerSession
from app.models.active_timer import ActiveTimer
from app.models.plan import Plan
from app.schemas.timer import (
    TimerCreate, TimerStart, TimerUpdate, TimerResponse,
    TimerTodayStats, ActiveTimerResponse
)


class TimerService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Active Timer Management
    async def get_active_timers(self) -> List[ActiveTimerResponse]:
        """Get all active timers"""
        query = select(ActiveTimer).order_by(ActiveTimer.created_at.desc())
        result = await self.db.execute(query)
        timers = list(result.scalars().all())
        
        # Populate plan information
        response = []
        for timer in timers:
            timer_data = {
                "id": timer.id,
                "planId": timer.plan_id,
                "planTitle": None,
                "planDescription": None,
                "title": timer.title,
                "elapsed": timer.elapsed,
                "isRunning": timer.is_running,
                "startTime": timer.start_time
            }
            
            if timer.plan_id:
                plan_result = await self.db.execute(
                    select(Plan).where(Plan.id == timer.plan_id)
                )
                plan = plan_result.scalar_one_or_none()
                if plan:
                    timer_data["planTitle"] = plan.title
                    timer_data["planDescription"] = plan.description
            
            response.append(ActiveTimerResponse(**timer_data))
        
        return response
    
    async def create_timer(self, data: TimerCreate) -> ActiveTimerResponse:
        """Create a new timer"""
        timer = ActiveTimer(
            plan_id=data.plan_id,
            title=data.title,
            elapsed=0,
            is_running=False
        )
        
        self.db.add(timer)
        await self.db.commit()
        await self.db.refresh(timer)
        
        # Get plan info if exists
        plan_title = None
        plan_description = None
        if timer.plan_id:
            plan_result = await self.db.execute(
                select(Plan).where(Plan.id == timer.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_title = plan.title
                plan_description = plan.description
        
        return ActiveTimerResponse(
            id=timer.id,
            planId=timer.plan_id,
            planTitle=plan_title,
            planDescription=plan_description,
            title=timer.title,
            elapsed=timer.elapsed,
            isRunning=timer.is_running,
            startTime=timer.start_time
        )
    
    async def start_timer(self, timer_id: int) -> Optional[ActiveTimerResponse]:
        """Start a timer"""
        result = await self.db.execute(
            select(ActiveTimer).where(ActiveTimer.id == timer_id)
        )
        timer = result.scalar_one_or_none()
        
        if not timer:
            return None
        
        timer.is_running = True
        timer.start_time = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(timer)
        
        # Get plan info
        plan_title = None
        plan_description = None
        if timer.plan_id:
            plan_result = await self.db.execute(
                select(Plan).where(Plan.id == timer.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_title = plan.title
                plan_description = plan.description
        
        return ActiveTimerResponse(
            id=timer.id,
            planId=timer.plan_id,
            planTitle=plan_title,
            planDescription=plan_description,
            title=timer.title,
            elapsed=timer.elapsed,
            isRunning=timer.is_running,
            startTime=timer.start_time
        )
    
    async def pause_timer(self, timer_id: int) -> Optional[ActiveTimerResponse]:
        """Pause a timer"""
        result = await self.db.execute(
            select(ActiveTimer).where(ActiveTimer.id == timer_id)
        )
        timer = result.scalar_one_or_none()
        
        if not timer:
            return None
        
        if timer.is_running and timer.start_time:
            # Calculate elapsed time since start
            elapsed_since_start = int((datetime.utcnow() - timer.start_time).total_seconds())
            timer.elapsed += elapsed_since_start
        
        timer.is_running = False
        timer.start_time = None
        
        await self.db.commit()
        await self.db.refresh(timer)
        
        # Get plan info
        plan_title = None
        plan_description = None
        if timer.plan_id:
            plan_result = await self.db.execute(
                select(Plan).where(Plan.id == timer.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_title = plan.title
                plan_description = plan.description
        
        return ActiveTimerResponse(
            id=timer.id,
            planId=timer.plan_id,
            planTitle=plan_title,
            planDescription=plan_description,
            title=timer.title,
            elapsed=timer.elapsed,
            isRunning=timer.is_running,
            startTime=timer.start_time
        )
    
    async def stop_timer(self, timer_id: int, data: Optional[TimerUpdate] = None) -> Optional[TimerResponse]:
        """Stop a timer and save as session"""
        result = await self.db.execute(
            select(ActiveTimer).where(ActiveTimer.id == timer_id)
        )
        timer = result.scalar_one_or_none()
        
        if not timer:
            return None
        
        # Calculate final elapsed time
        final_elapsed = timer.elapsed
        if timer.is_running and timer.start_time:
            elapsed_since_start = int((datetime.utcnow() - timer.start_time).total_seconds())
            final_elapsed += elapsed_since_start
        
        # Create timer session
        session = TimerSession(
            plan_id=timer.plan_id,
            start_time=timer.created_at,
            end_time=datetime.utcnow(),
            duration=final_elapsed,
            notes=data.notes if data else None,
            focus_score=Decimal('85.0')  # Default focus score
        )
        
        self.db.add(session)
        
        # Delete active timer
        await self.db.delete(timer)
        
        await self.db.commit()
        await self.db.refresh(session)
        
        # Get plan info
        plan_title = None
        if session.plan_id:
            plan_result = await self.db.execute(
                select(Plan).where(Plan.id == session.plan_id)
            )
            plan = plan_result.scalar_one_or_none()
            if plan:
                plan_title = plan.title
                # Update plan's actual duration
                plan.actual_duration = (plan.actual_duration or 0) + (final_elapsed // 60)
                await self.db.commit()
        
        session.plan_title = plan_title
        
        return session
    
    async def delete_timer(self, timer_id: int) -> bool:
        """Delete a timer"""
        result = await self.db.execute(
            select(ActiveTimer).where(ActiveTimer.id == timer_id)
        )
        timer = result.scalar_one_or_none()
        
        if not timer:
            return False
        
        await self.db.delete(timer)
        await self.db.commit()
        return True
    
    # Timer Sessions
    async def get_sessions(
        self,
        skip: int = 0,
        limit: int = 100,
        plan_id: Optional[int] = None,
        project_id: Optional[int] = None,
        date: Optional[date] = None
    ) -> List[TimerResponse]:
        """Get timer sessions, optionally filtered by date"""
        query = select(TimerSession)
        
        if plan_id:
            query = query.where(TimerSession.plan_id == plan_id)
        if project_id:
            query = query.where(TimerSession.project_id == project_id)
        if date:
            # For SQLite, use date() function instead of CAST
            query = query.where(func.date(TimerSession.start_time) == date)
        
        query = query.order_by(TimerSession.start_time.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        sessions = list(result.scalars().all())
        
        # Populate plan titles
        for session in sessions:
            if session.plan_id:
                plan_result = await self.db.execute(
                    select(Plan).where(Plan.id == session.plan_id)
                )
                plan = plan_result.scalar_one_or_none()
                if plan:
                    session.plan_title = plan.title
        
        return sessions
    
    async def get_today_stats(self) -> TimerTodayStats:
        """Get today's statistics"""
        today = date.today()
        
        query = select(
            func.sum(TimerSession.duration).label('total_duration'),
            func.count(TimerSession.id).label('session_count'),
            func.avg(TimerSession.focus_score).label('focus_score_avg')
        ).where(
            func.date(TimerSession.start_time) == today
        )
        
        result = await self.db.execute(query)
        row = result.first()
        
        return TimerTodayStats(
            total_duration=int(row.total_duration or 0),
            session_count=int(row.session_count or 0),
            focus_score_avg=row.focus_score_avg
        )
