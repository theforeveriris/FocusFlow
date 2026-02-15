from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base


class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Priority matrix: urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important
    priority_matrix = Column(String(30), default="not_urgent_important")
    status = Column(String(20), default="todo")  # todo, in_progress, completed, cancelled
    
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # minutes
    actual_duration = Column(Integer, default=0)  # minutes
    
    tags = Column(JSON, default=list)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="plans")
    children = relationship("Plan", backref="parent", remote_side=[id])
    timer_sessions = relationship("TimerSession", back_populates="plan")
