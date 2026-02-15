from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import List, Optional
from datetime import datetime
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate
from app.services.project_service import ProjectService


class PlanService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exclude_completed: bool = True
    ) -> List[Plan]:
        """Get all plans with filters"""
        query = select(Plan).where(Plan.parent_id.is_(None))
        
        # Exclude completed plans by default
        if exclude_completed:
            query = query.where(Plan.status != "completed")
        
        if project_id:
            query = query.where(Plan.project_id == project_id)
        if status:
            query = query.where(Plan.status == status)
        if priority:
            query = query.where(Plan.priority_matrix == priority)
        
        # Filter by creation date range
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.where(Plan.created_at >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.where(Plan.created_at <= end_dt)
            except ValueError:
                pass
        
        query = query.order_by(Plan.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, plan_id: int) -> Optional[Plan]:
        """Get plan by ID"""
        result = await self.db.execute(select(Plan).where(Plan.id == plan_id))
        return result.scalar_one_or_none()
    
    async def get_tree(self, project_id: Optional[int] = None) -> List[Plan]:
        """Get plan tree structure"""
        query = select(Plan).where(Plan.parent_id.is_(None))
        if project_id:
            query = query.where(Plan.project_id == project_id)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create(self, plan_data: PlanCreate) -> Plan:
        """Create new plan"""
        plan = Plan(**plan_data.model_dump())
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        
        # Update project progress if linked
        if plan.project_id:
            project_service = ProjectService(self.db)
            await project_service.update_progress(plan.project_id)
        
        return plan
    
    async def update(self, plan_id: int, plan_data: PlanUpdate) -> Optional[Plan]:
        """Update plan"""
        plan = await self.get_by_id(plan_id)
        if not plan:
            return None
        
        old_project_id = plan.project_id
        update_data = plan_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        await self.db.commit()
        await self.db.refresh(plan)
        
        # Update project progress
        project_service = ProjectService(self.db)
        if old_project_id and old_project_id != plan.project_id:
            await project_service.update_progress(old_project_id)
        if plan.project_id:
            await project_service.update_progress(plan.project_id)
        
        return plan
    
    async def delete(self, plan_id: int) -> bool:
        """Delete plan and its children"""
        plan = await self.get_by_id(plan_id)
        if not plan:
            return False
        
        project_id = plan.project_id
        
        # Delete children recursively
        await self._delete_children(plan_id)
        
        await self.db.delete(plan)
        await self.db.commit()
        
        # Update project progress
        if project_id:
            project_service = ProjectService(self.db)
            await project_service.update_progress(project_id)
        
        return True
    
    async def _delete_children(self, parent_id: int) -> None:
        """Recursively delete child plans"""
        result = await self.db.execute(select(Plan).where(Plan.parent_id == parent_id))
        children = result.scalars().all()
        
        for child in children:
            await self._delete_children(child.id)
            await self.db.delete(child)
    
    async def check_time_conflict(
        self,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None
    ) -> List[Plan]:
        """Check for time conflicts"""
        query = select(Plan).where(
            Plan.status.notin_(["completed", "cancelled"]),
            or_(
                and_(Plan.start_time <= start_time, Plan.end_time > start_time),
                and_(Plan.start_time < end_time, Plan.end_time >= end_time),
                and_(Plan.start_time >= start_time, Plan.end_time <= end_time)
            )
        )
        
        if exclude_id:
            query = query.where(Plan.id != exclude_id)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
