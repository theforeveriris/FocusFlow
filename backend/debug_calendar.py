"""
调试日历 API
"""
import asyncio
from datetime import date
from app.database import get_db
from app.services.timer_service import TimerService

async def test_get_sessions_by_date():
    """测试按日期获取会话"""
    async for db in get_db():
        try:
            service = TimerService(db)
            
            today = date.today()
            print(f"查询日期: {today}")
            
            sessions = await service.get_sessions(date=today)
            
            print(f"\n找到 {len(sessions)} 个会话")
            
            for session in sessions:
                print(f"\n会话 ID: {session.id}")
                print(f"  计划: {getattr(session, 'plan_title', None)}")
                print(f"  开始: {session.start_time}")
                print(f"  结束: {session.end_time}")
                print(f"  时长: {session.duration}秒")
                
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        
        break

if __name__ == "__main__":
    asyncio.run(test_get_sessions_by_date())
