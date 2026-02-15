"""
记账功能演示脚本
"""
import asyncio
from datetime import date
from decimal import Decimal
from app.database import AsyncSessionLocal
from app.services.accounting_service import AccountingService
from app.services.account_service import AccountService
from app.schemas.accounting import TransactionCreate


async def demo():
    async with AsyncSessionLocal() as db:
        account_service = AccountService(db)
        accounting_service = AccountingService(db)
        
        print("=" * 60)
        print("FocusFlow 记账功能演示")
        print("=" * 60)
        
        # 1. 查看账户汇总
        print("\n📊 账户汇总：")
        summary = await account_service.get_summary()
        print(f"  总资产：¥{summary.total_assets}")
        print(f"  总负债：¥{summary.total_liabilities}")
        print(f"  净资产：¥{summary.net_worth}")
        
        print("\n💰 资产账户：")
        for acc in summary.asset_accounts:
            print(f"  - {acc.name}: ¥{acc.balance} (可用: ¥{acc.available_balance})")
        
        print("\n💳 负债账户：")
        for acc in summary.liability_accounts:
            print(f"  - {acc.name}: ¥{acc.balance} (欠款: ¥{abs(acc.balance)})")
        
        # 2. 演示收入
        print("\n" + "=" * 60)
        print("💵 记录收入：工资 ¥15,000")
        income = TransactionCreate(
            type="income",
            amount=Decimal("15000.00"),
            to_account_id=2,  # 工商银行
            transaction_date=date.today(),
            description="工资"
        )
        await accounting_service.create(income)
        print("  ✓ 收入已记录")
        
        # 3. 演示支出
        print("\n💸 记录支出：午餐 ¥50")
        expense = TransactionCreate(
            type="expense",
            amount=Decimal("50.00"),
            from_account_id=3,  # 微信支付
            transaction_date=date.today(),
            description="午餐"
        )
        await accounting_service.create(expense)
        print("  ✓ 支出已记录")
        
        # 4. 演示转账
        print("\n🔄 账户转账：工商银行 → 微信支付 ¥500")
        transfer = TransactionCreate(
            type="transfer",
            amount=Decimal("500.00"),
            from_account_id=2,  # 工商银行
            to_account_id=3,  # 微信支付
            transaction_date=date.today(),
            description="转账到微信"
        )
        await accounting_service.create(transfer)
        print("  ✓ 转账完成")
        
        # 5. 演示还款
        print("\n💳 信用卡还款：工商银行 → 招商银行信用卡 ¥1,200")
        repayment = TransactionCreate(
            type="repayment",
            amount=Decimal("1200.00"),
            from_account_id=2,  # 工商银行
            to_account_id=5,  # 招商银行信用卡
            transaction_date=date.today(),
            description="还信用卡"
        )
        await accounting_service.create(repayment)
        print("  ✓ 还款完成")
        
        # 6. 查看更新后的账户汇总
        print("\n" + "=" * 60)
        print("📊 更新后的账户汇总：")
        summary = await account_service.get_summary()
        print(f"  总资产：¥{summary.total_assets}")
        print(f"  总负债：¥{summary.total_liabilities}")
        print(f"  净资产：¥{summary.net_worth}")
        
        print("\n💰 资产账户：")
        for acc in summary.asset_accounts:
            print(f"  - {acc.name}: ¥{acc.balance}")
        
        print("\n💳 负债账户：")
        for acc in summary.liability_accounts:
            status = "已还清" if acc.balance >= 0 else f"欠款 ¥{abs(acc.balance)}"
            print(f"  - {acc.name}: {status}")
        
        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
