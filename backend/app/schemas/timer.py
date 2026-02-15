from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TimerCreate(BaseModel):
    plan_id: Optional[int] = None
    title: Optional[str] = None


class TimerStart(BaseModel):
    plan_id: Optional[int] = None
    project_id: Optional[int] = None
    is_zen_mode: bool = False


class TimerUpdate(BaseModel):
    notes: Optional[str] = None


class ActiveTimerResponse(BaseModel):
    id: int
    planId: Optional[int] = None
    planTitle: Optional[str] = None
    planDescription: Optional[str] = None
    title: Optional[str] = None
    elapsed: int  # seconds
    isRunning: bool
    startTime: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TimerResponse(BaseModel):
    id: int
    plan_id: Optional[int]
    project_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    duration: int  # seconds
    interrupt_count: int
    focus_score: Optional[Decimal]
    notes: Optional[str]
    is_zen_mode: bool
    created_at: datetime
    plan_title: Optional[str] = None
    project_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class TimerTodayStats(BaseModel):
    total_duration: int  # seconds
    session_count: int
    focus_score_avg: Optional[Decimal]

