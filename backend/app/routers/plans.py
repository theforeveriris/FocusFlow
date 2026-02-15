from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from app.services.plan_service import PlanService

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("", response_model=List[PlanResponse])
async def get_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    exclude_completed: bool = Query(True, description="Exclude completed plans"),
    db: AsyncSession = Depends(get_db)
):
    """Get all plans with filters"""
    service = PlanService(db)
    plans = await service.get_all(
        skip=skip,
        limit=limit,
        project_id=project_id,
        status=status,
        priority=priority,
        start_date=start_date,
        end_date=end_date,
        exclude_completed=exclude_completed
    )
    return plans


@router.get("/tree", response_model=List[PlanResponse])
async def get_plan_tree(
    project_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get plan tree structure"""
    service = PlanService(db)
    return await service.get_tree(project_id=project_id)


@router.post("", response_model=PlanResponse, status_code=201)
async def create_plan(
    plan: PlanCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new plan"""
    service = PlanService(db)
    
    # Check time conflict if start/end time provided
    if plan.start_time and plan.end_time:
        conflicts = await service.check_time_conflict(plan.start_time, plan.end_time)
        if conflicts:
            raise HTTPException(
                status_code=400,
                detail=f"Time conflict with existing plans: {[p.title for p in conflicts]}"
            )
    
    return await service.create(plan)


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get plan by ID"""
    service = PlanService(db)
    plan = await service.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan: PlanUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update plan"""
    service = PlanService(db)
    
    # Check time conflict if start/end time provided
    if plan.start_time and plan.end_time:
        conflicts = await service.check_time_conflict(
            plan.start_time,
            plan.end_time,
            exclude_id=plan_id
        )
        if conflicts:
            raise HTTPException(
                status_code=400,
                detail=f"Time conflict with existing plans: {[p.title for p in conflicts]}"
            )
    
    updated = await service.update(plan_id, plan)
    if not updated:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete plan"""
    service = PlanService(db)
    success = await service.delete(plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}


@router.patch("/{plan_id}/status")
async def update_plan_status(
    plan_id: int,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    """Update plan status"""
    service = PlanService(db)
    updated = await service.update(plan_id, PlanUpdate(status=status))
    if not updated:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated
