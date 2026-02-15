from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date, datetime, timedelta
from app.database import get_db
from app.services.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/overview")
async def get_overview(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get overview statistics"""
    service = StatisticsService(db)
    return await service.get_overview(start_date, end_date)


@router.get("/time-trend")
async def get_time_trend(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get time trend data"""
    service = StatisticsService(db)
    return await service.get_time_trend(start_date, end_date)


@router.get("/plan-completion")
async def get_plan_completion(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get plan completion statistics"""
    service = StatisticsService(db)
    return await service.get_plan_completion(start_date, end_date)


@router.get("/project-time")
async def get_project_time(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get project time distribution"""
    service = StatisticsService(db)
    return await service.get_project_time(start_date, end_date)


@router.get("/focus-trend")
async def get_focus_trend(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get focus score trend"""
    service = StatisticsService(db)
    return await service.get_focus_trend(start_date, end_date)


@router.get("/heatmap")
async def get_heatmap(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get time heatmap data"""
    service = StatisticsService(db)
    return await service.get_heatmap(start_date, end_date)


@router.get("/finance-trend")
async def get_finance_trend(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get finance trend data"""
    service = StatisticsService(db)
    return await service.get_finance_trend(start_date, end_date)


@router.get("/expense-category")
async def get_expense_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get expense category distribution"""
    service = StatisticsService(db)
    return await service.get_expense_category(start_date, end_date)


@router.get("/daily-distribution")
async def get_daily_distribution(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get daily time distribution (by weekday)"""
    service = StatisticsService(db)
    return await service.get_daily_distribution(start_date, end_date)


@router.get("/priority-distribution")
async def get_priority_distribution(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get plan priority distribution"""
    service = StatisticsService(db)
    return await service.get_priority_distribution(start_date, end_date)
