"""
修复 transactions 表 - 添加 updated_at 字段
"""
import asyncio
from sqlalchemy import text
from app.database import engine


async def fix_table():
    """修复 transactions 表"""
    async with engine.begin() as conn:
        # 1. 创建新表
        await conn.execute(text("""
            CREATE TABLE transactions_new (
                id INTEGER PRIMARY KEY,
                type VARCHAR(20) NOT NULL,
                amount NUMERIC(10, 2) NOT NULL,
                category_id INTEGER REFERENCES categories(id),
                from_account_id INTEGER REFERENCES accounts(id),
                to_account_id INTEGER REFERENCES accounts(id),
                plan_id INTEGER REFERENCES plans(id),
                project_id INTEGER REFERENCES projects(id),
                transaction_date DATE NOT NULL,
                description VARCHAR(500),
                tags JSON,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✓ Created new transactions table")
        
        # 2. 复制数据
        await conn.execute(text("""
            INSERT INTO transactions_new 
            (id, type, amount, category_id, from_account_id, to_account_id, 
             plan_id, project_id, transaction_date, description, tags, created_at, updated_at)
            SELECT 
                id, type, amount, category_id, from_account_id, to_account_id,
                plan_id, project_id, transaction_date, description, tags, created_at, created_at
            FROM transactions
        """))
        print("✓ Copied data to new table")
        
        # 3. 删除旧表
        await conn.execute(text("DROP TABLE transactions"))
        print("✓ Dropped old table")
        
        # 4. 重命名新表
        await conn.execute(text("ALTER TABLE transactions_new RENAME TO transactions"))
        print("✓ Renamed new table")
        
        # 5. 创建索引
        await conn.execute(text("CREATE INDEX ix_transactions_id ON transactions (id)"))
        print("✓ Created index")
        
        await conn.commit()
    
    print("\n✅ Table fixed successfully!")


if __name__ == "__main__":
    print("Fixing transactions table...")
    asyncio.run(fix_table())
