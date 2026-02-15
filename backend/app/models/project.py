from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#3b82f6")
    icon = Column(String(50), nullable=True)
    status = Column(String(20), default="active")  # active, archived, deleted
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress = Column(Numeric(5, 2), default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    plans = relationship("Plan", back_populates="project")
    timer_sessions = relationship("TimerSession", back_populates="project")
    transactions = relationship("Transaction", back_populates="project")
