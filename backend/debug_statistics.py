"""
调试统计服务
"""
import asyncio
from datetime import date
from app.database import get_db
from app.services.statistics_service import StatisticsService

async def test_overview():
    """测试概览功能"""
    async for db in get_db():
        try:
            service = StatisticsService(db)
            
            end_date = date.today()
            start_date = date(end_date.year, end_date.month, 1)
            
            print(f"测试日期范围: {start_date} 到 {end_date}")
            
            result = await service.get_overview(start_date, end_date)
            
            print("\n概览数据:")
            for key, value in result.items():
                print(f"  {key}: {value}")
                
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        
        break

if __name__ == "__main__":
    asyncio.run(test_overview())
