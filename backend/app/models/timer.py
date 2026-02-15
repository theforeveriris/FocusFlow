from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, Text, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base


class TimerSession(Base):
    __tablename__ = "timer_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, default=0)  # seconds
    interrupt_count = Column(Integer, default=0)
    focus_score = Column(Numeric(4, 2), nullable=True)  # 0-100
    notes = Column(Text, nullable=True)
    is_zen_mode = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    plan = relationship("Plan", back_populates="timer_sessions")
    project = relationship("Project", back_populates="timer_sessions")
