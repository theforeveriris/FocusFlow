from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, func
from app.database import Base


class Account(Base):
    """账户模型 - 资金池和负债池"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 账户名称
    type = Column(String(20), nullable=False)  # asset(资产), liability(负债)
    sub_type = Column(String(50), nullable=True)  # bank_card, wechat, alipay, credit_card, loan, etc.
    balance = Column(Numeric(12, 2), default=0, nullable=False)  # 当前余额
    initial_balance = Column(Numeric(12, 2), default=0, nullable=False)  # 初始余额
    credit_limit = Column(Numeric(12, 2), nullable=True)  # 信用额度（信用卡）
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)  # 是否启用
    is_default = Column(Boolean, default=False, nullable=False)  # 是否默认账户
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
