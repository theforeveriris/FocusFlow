from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PlanBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    project_id: Optional[int] = None
    priority_matrix: str = Field(default="not_urgent_important")
    status: str = Field(default="todo")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_duration: Optional[int] = None  # minutes
    tags: List[str] = []


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    project_id: Optional[int] = None
    priority_matrix: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    tags: Optional[List[str]] = None


class PlanResponse(PlanBase):
    id: int
    actual_duration: int
    created_at: datetime
    updated_at: datetime
    project_name: Optional[str] = None
    children_count: int = 0
    
    class Config:
        from_attributes = True


class PlanTree(PlanResponse):
    children: List["PlanTree"] = []
    
    class Config:
        from_attributes = True
