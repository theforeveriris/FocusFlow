"""
数据库迁移脚本 - 添加账户功能
"""
import asyncio
from sqlalchemy import text
from app.database import engine
from app.models import Account
from app.database import Base


async def migrate():
    """执行数据库迁移"""
    async with engine.begin() as conn:
        # 创建账户表
        await conn.run_sync(Base.metadata.create_all)
        
        # 检查 transactions 表是否需要更新
        # 添加新字段
        try:
            await conn.execute(text("""
                ALTER TABLE transactions 
                ADD COLUMN from_account_id INTEGER REFERENCES accounts(id)
            """))
            print("✓ Added from_account_id column")
        except Exception as e:
            print(f"from_account_id column may already exist: {e}")
        
        try:
            await conn.execute(text("""
                ALTER TABLE transactions 
                ADD COLUMN to_account_id INTEGER REFERENCES accounts(id)
            """))
            print("✓ Added to_account_id column")
        except Exception as e:
            print(f"to_account_id column may already exist: {e}")
        
        try:
            await conn.execute(text("""
                ALTER TABLE transactions 
                ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            """))
            print("✓ Added updated_at column")
        except Exception as e:
            print(f"updated_at column may already exist: {e}")
        
        # 迁移旧的 account_id 数据到新字段
        try:
            # 对于支出类型，将 account_id 迁移到 from_account_id
            await conn.execute(text("""
                UPDATE transactions 
                SET from_account_id = account_id 
                WHERE type = 'expense' AND account_id IS NOT NULL
            """))
            
            # 对于收入类型，将 account_id 迁移到 to_account_id
            await conn.execute(text("""
                UPDATE transactions 
                SET to_account_id = account_id 
                WHERE type = 'income' AND account_id IS NOT NULL
            """))
            print("✓ Migrated old account_id data")
        except Exception as e:
            print(f"Data migration may have already been done: {e}")
        
        # 创建示例账户
        try:
            await conn.execute(text("""
                INSERT INTO accounts (name, type, sub_type, balance, initial_balance, icon, color, is_active, is_default)
                VALUES 
                    ('现金', 'asset', 'cash', 1000.00, 1000.00, 'wallet', '#10b981', 1, 1),
                    ('工商银行', 'asset', 'bank_card', 5000.00, 5000.00, 'building-2', '#3b82f6', 1, 0),
                    ('微信支付', 'asset', 'wechat', 500.00, 500.00, 'message-circle', '#10b981', 1, 0),
                    ('支付宝', 'asset', 'alipay', 800.00, 800.00, 'smartphone', '#1890ff', 1, 0),
                    ('招商银行信用卡', 'liability', 'credit_card', -1200.00, 0.00, 'credit-card', '#ef4444', 1, 0),
                    ('花呗', 'liability', 'bnpl', -300.00, 0.00, 'shopping-bag', '#f59e0b', 1, 0)
            """))
            print("✓ Created sample accounts")
        except Exception as e:
            print(f"Sample accounts may already exist: {e}")
        
        await conn.commit()
    
    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    print("Starting database migration...")
    asyncio.run(migrate())
