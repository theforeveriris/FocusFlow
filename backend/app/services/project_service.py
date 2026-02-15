from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.models.project import Project
from app.models.plan import Plan
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects with plan count"""
        result = await self.db.execute(
            select(Project).where(Project.status != "deleted").offset(skip).limit(limit)
        )
        projects = result.scalars().all()
        
        # Get plan count for each project
        for project in projects:
            plan_count_result = await self.db.execute(
                select(func.count(Plan.id)).where(Plan.project_id == project.id)
            )
            project.plan_count = plan_count_result.scalar()
        
        return list(projects)
    
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id, Project.status != "deleted")
        )
        return result.scalar_one_or_none()
    
    async def create(self, project_data: ProjectCreate) -> Project:
        """Create new project"""
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def update(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Update project"""
        project = await self.get_by_id(project_id)
        if not project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def delete(self, project_id: int) -> bool:
        """Soft delete project"""
        project = await self.get_by_id(project_id)
        if not project:
            return False
        
        project.status = "deleted"
        await self.db.commit()
        return True
    
    async def update_progress(self, project_id: int) -> None:
        """Update project progress based on plans"""
        result = await self.db.execute(
            select(func.count(Plan.id)).where(
                Plan.project_id == project_id,
                Plan.status != "cancelled"
            )
        )
        total_plans = result.scalar()
        
        if total_plans == 0:
            return
        
        result = await self.db.execute(
            select(func.count(Plan.id)).where(
                Plan.project_id == project_id,
                Plan.status == "completed"
            )
        )
        completed_plans = result.scalar()
        
        project = await self.get_by_id(project_id)
        if project:
            project.progress = round((completed_plans / total_plans) * 100, 2)
            await self.db.commit()
