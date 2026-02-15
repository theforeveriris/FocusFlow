from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class ActiveTimer(Base):
    __tablename__ = "active_timers"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    title = Column(String(255), nullable=True)
    elapsed = Column(Integer, default=0)  # seconds
    is_running = Column(Boolean, default=False)
    start_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    plan = relationship("Plan")
