"""
测试账户交易查询
"""
import asyncio
from app.database import AsyncSessionLocal
from app.services.accounting_service import AccountingService


async def test():
    async with AsyncSessionLocal() as db:
        service = AccountingService(db)
        
        print("=" * 60)
        print("测试账户交易查询")
        print("=" * 60)
        
        # 查询账户1的交易
        print("\n查询账户 ID=1 的交易：")
        transactions = await service.get_transactions(account_id=1)
        print(f"找到 {len(transactions)} 条交易记录")
        
        for t in transactions:
            print(f"\n交易 ID: {t.id}")
            print(f"  类型: {t.type}")
            print(f"  金额: {t.amount}")
            print(f"  日期: {t.transaction_date}")
            print(f"  描述: {t.description}")
            print(f"  转出账户: {t.from_account_id} - {getattr(t, 'from_account_name', 'N/A')}")
            print(f"  转入账户: {t.to_account_id} - {getattr(t, 'to_account_name', 'N/A')}")
        
        # 查询所有交易
        print("\n\n查询所有交易：")
        all_transactions = await service.get_transactions()
        print(f"总共 {len(all_transactions)} 条交易记录")


if __name__ == "__main__":
    asyncio.run(test())
