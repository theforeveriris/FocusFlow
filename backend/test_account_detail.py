"""
测试账户详情 API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_account_detail():
    """测试账户详情端点"""
    print("=" * 60)
    print("测试账户详情 API")
    print("=" * 60)
    
    # 1. 获取所有账户
    print("\n[1] 获取账户列表...")
    try:
        response = requests.get(f"{BASE_URL}/accounts", timeout=10)
        if response.status_code == 200:
            accounts = response.json()
            print(f"✓ 找到 {len(accounts)} 个账户")
            
            if len(accounts) == 0:
                print("⚠ 没有账户，请先创建账户")
                return
            
            # 2. 测试每个账户的详情
            print("\n[2] 测试账户详情...")
            for account in accounts[:3]:  # 只测试前3个
                account_id = account['id']
                account_name = account['name']
                
                print(f"\n测试账户: {account_name} (ID: {account_id})")
                
                # 获取账户详情
                detail_response = requests.get(
                    f"{BASE_URL}/accounts/{account_id}",
                    timeout=10
                )
                
                if detail_response.status_code == 200:
                    detail = detail_response.json()
                    print(f"  ✓ 账户详情: {json.dumps(detail, ensure_ascii=False, indent=2)}")
                    
                    # 验证必需字段
                    required_fields = ['id', 'name', 'type', 'balance']
                    missing_fields = [f for f in required_fields if f not in detail]
                    
                    if missing_fields:
                        print(f"  ✗ 缺少字段: {missing_fields}")
                    else:
                        print(f"  ✓ 所有必需字段都存在")
                    
                    # 获取该账户的交易记录
                    trans_response = requests.get(
                        f"{BASE_URL}/accounting/transactions",
                        params={'account_id': account_id},
                        timeout=10
                    )
                    
                    if trans_response.status_code == 200:
                        transactions = trans_response.json()
                        print(f"  ✓ 交易记录: {len(transactions)} 条")
                        
                        # 检查交易记录的账户名称字段
                        if transactions:
                            first_trans = transactions[0]
                            has_account_names = (
                                'from_account_name' in first_trans or 
                                'to_account_name' in first_trans
                            )
                            if has_account_names:
                                print(f"  ✓ 交易记录包含账户名称")
                            else:
                                print(f"  ⚠ 交易记录缺少账户名称字段")
                    else:
                        print(f"  ✗ 获取交易记录失败: {trans_response.status_code}")
                        
                else:
                    print(f"  ✗ 获取账户详情失败: {detail_response.status_code}")
                    print(f"  响应: {detail_response.text}")
                    
        else:
            print(f"✗ 获取账户列表失败: {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_account_detail()
