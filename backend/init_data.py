"""
Initialize database with sample data
"""
import asyncio
from app.database import init_db, AsyncSessionLocal
from app.models.project import Project
from app.models.plan import Plan
from app.models.transaction import Category, Transaction
from app.models.timer import TimerSession
from datetime import datetime, timedelta, date


async def init_sample_data():
    """Initialize sample data"""
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Create sample projects
        projects = [
            Project(
                name="个人学习",
                description="学习新技能和个人提升",
                color="#3b82f6",
                status="active",
                progress=45
            ),
            Project(
                name="工作任务",
                description="日常工作任务管理",
                color="#ef4444",
                status="active",
                progress=60
            ),
            Project(
                name="健身计划",
                description="保持健康和锻炼",
                color="#10b981",
                status="active",
                progress=30
            )
        ]
        
        for project in projects:
            session.add(project)
        
        await session.flush()
        
        # Create sample plans
        plans = [
            Plan(
                title="完成Vue3项目",
                description="学习Vue3 Composition API并实践",
                project_id=projects[0].id,
                priority_matrix="not_urgent_important",
                status="in_progress",
                estimated_duration=120,
                actual_duration=60
            ),
            Plan(
                title="阅读技术书籍",
                description="阅读《Clean Code》",
                project_id=projects[0].id,
                priority_matrix="not_urgent_important",
                status="todo",
                estimated_duration=60
            ),
            Plan(
                title="完成周报",
                description="整理本周工作进度",
                project_id=projects[1].id,
                priority_matrix="urgent_important",
                status="completed",
                estimated_duration=30,
                actual_duration=25
            ),
            Plan(
                title="晨跑5公里",
                description="早起跑步锻炼",
                project_id=projects[2].id,
                priority_matrix="not_urgent_important",
                status="todo",
                estimated_duration=45
            )
        ]
        
        for plan in plans:
            session.add(plan)
        
        await session.flush()
        
        # Create sample categories
        categories = [
            Category(name="餐饮", type="expense", icon="coffee", color="#f59e0b"),
            Category(name="交通", type="expense", icon="car", color="#3b82f6"),
            Category(name="购物", type="expense", icon="shopping-cart", color="#ef4444"),
            Category(name="工资", type="income", icon="briefcase", color="#10b981"),
            Category(name="投资", type="income", icon="trending-up", color="#8b5cf6")
        ]
        
        for category in categories:
            session.add(category)
        
        await session.flush()
        
        # Create sample transactions
        transactions = [
            Transaction(
                type="income",
                amount=15000.00,
                category_id=categories[3].id,
                transaction_date=date.today().replace(day=1),
                description="本月工资"
            ),
            Transaction(
                type="expense",
                amount=35.50,
                category_id=categories[0].id,
                transaction_date=date.today(),
                description="午餐"
            ),
            Transaction(
                type="expense",
                amount=120.00,
                category_id=categories[1].id,
                transaction_date=date.today() - timedelta(days=1),
                description="打车"
            ),
            Transaction(
                type="expense",
                amount=299.00,
                category_id=categories[2].id,
                transaction_date=date.today() - timedelta(days=2),
                description="买书"
            )
        ]
        
        for transaction in transactions:
            session.add(transaction)
        
        # Create sample timer sessions
        now = datetime.now()
        sessions = [
            TimerSession(
                plan_id=plans[0].id,
                project_id=projects[0].id,
                start_time=now - timedelta(hours=2),
                end_time=now - timedelta(hours=1, minutes=30),
                duration=1800,
                focus_score=85.5,
                notes="专注学习Vue3"
            ),
            TimerSession(
                plan_id=plans[2].id,
                project_id=projects[1].id,
                start_time=now - timedelta(days=1, hours=3),
                end_time=now - timedelta(days=1, hours=2, minutes=35),
                duration=1500,
                focus_score=92.0,
                notes="完成周报"
            ),
            TimerSession(
                plan_id=plans[0].id,
                project_id=projects[0].id,
                start_time=now - timedelta(days=2, hours=1),
                end_time=now - timedelta(days=2, hours=0, minutes=45),
                duration=900,
                focus_score=78.5,
                interrupt_count=1,
                notes="阅读文档"
            )
        ]
        
        for session_obj in sessions:
            session.add(session_obj)
        
        await session.commit()
        print("Sample data initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_sample_data())
