from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.schemas.timer import (
    TimerCreate, TimerStart, TimerUpdate, TimerResponse, 
    TimerTodayStats, ActiveTimerResponse
)
from app.services.timer_service import TimerService

router = APIRouter(prefix="/timer", tags=["timer"])


@router.get("/active", response_model=List[ActiveTimerResponse])
async def get_active_timers(
    db: AsyncSession = Depends(get_db)
):
    """Get all active timers"""
    service = TimerService(db)
    return await service.get_active_timers()


@router.post("/create", response_model=ActiveTimerResponse, status_code=201)
async def create_timer(
    data: TimerCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new timer"""
    service = TimerService(db)
    return await service.create_timer(data)


@router.post("/{timer_id}/start", response_model=ActiveTimerResponse)
async def start_timer(
    timer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start a timer"""
    service = TimerService(db)
    timer = await service.start_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return timer


@router.post("/{timer_id}/pause", response_model=ActiveTimerResponse)
async def pause_timer(
    timer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Pause a timer"""
    service = TimerService(db)
    timer = await service.pause_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return timer


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(
    timer_id: int,
    data: Optional[TimerUpdate] = None,
    db: AsyncSession = Depends(get_db)
):
    """Stop a timer and save the session"""
    service = TimerService(db)
    session = await service.stop_timer(timer_id, data)
    if not session:
        raise HTTPException(status_code=404, detail="Timer not found")
    return session


@router.delete("/{timer_id}")
async def delete_timer(
    timer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a timer"""
    service = TimerService(db)
    success = await service.delete_timer(timer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Timer not found")
    return {"message": "Timer deleted successfully"}


@router.get("/sessions", response_model=List[TimerResponse])
async def get_timer_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    plan_id: Optional[int] = None,
    project_id: Optional[int] = None,
    date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get timer sessions, optionally filtered by date"""
    service = TimerService(db)
    sessions = await service.get_sessions(
        skip=skip,
        limit=limit,
        plan_id=plan_id,
        project_id=project_id,
        date=date
    )
    return sessions


@router.get("/stats/today", response_model=TimerTodayStats)
async def get_today_stats(
    db: AsyncSession = Depends(get_db)
):
    """Get today's timer statistics"""
    service = TimerService(db)
    return await service.get_today_stats()
