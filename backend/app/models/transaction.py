from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(10), nullable=False)  # income, expense
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    budget_limit = Column(Numeric(10, 2), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)  # income, expense, transfer, repayment
    amount = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # 账户相关
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # 转出账户
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # 转入账户
    
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    transaction_date = Column(Date, nullable=False)
    description = Column(String(500), nullable=True)
    tags = Column(JSON, default=list)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("Category")
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])
    plan = relationship("Plan")
    project = relationship("Project")
