import asyncio
from datetime import date
from decimal import Decimal
from app.database import AsyncSessionLocal
from app.services.accounting_service import AccountingService
from app.schemas.accounting import TransactionCreate


async def test_transfer():
    async with AsyncSessionLocal() as db:
        service = AccountingService(db)
        
        # 创建转账交易
        transfer_data = TransactionCreate(
            type="transfer",
            amount=Decimal("100.00"),
            from_account_id=1,
            to_account_id=3,
            transaction_date=date.today(),
            description="测试转账"
        )
        
        try:
            transaction = await service.create(transfer_data)
            print(f"✓ Transfer created: {transaction.id}")
            print(f"  Amount: {transaction.amount}")
            print(f"  From: {transaction.from_account_id}")
            print(f"  To: {transaction.to_account_id}")
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_transfer())
