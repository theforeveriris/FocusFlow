"""
测试时间追踪 API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_timer_api():
    print("=" * 60)
    print("测试时间追踪 API")
    print("=" * 60)
    
    # 1. 获取可用计划
    print("\n[1] 获取可用计划...")
    try:
        response = requests.get(f"{BASE_URL}/plans?exclude_completed=true")
        if response.status_code == 200:
            plans = response.json()
            print(f"✓ 找到 {len(plans)} 个计划")
            
            if plans:
                for plan in plans[:3]:
                    print(f"  - ID: {plan['id']}, 标题: {plan['title']}, 状态: {plan['status']}")
                
                # 2. 创建绑定计划的计时器
                print("\n[2] 创建绑定计划的计时器...")
                test_plan_id = plans[0]['id']
                
                create_response = requests.post(
                    f"{BASE_URL}/timer/create",
                    json={
                        "plan_id": test_plan_id,
                        "title": None
                    }
                )
                
                if create_response.status_code == 201:
                    timer = create_response.json()
                    print(f"✓ 计时器创建成功")
                    print(f"  Timer ID: {timer['id']}")
                    print(f"  Plan ID: {timer.get('planId')}")
                    print(f"  Plan Title: {timer.get('planTitle')}")
                    print(f"  Plan Description: {timer.get('planDescription')}")
                    
                    timer_id = timer['id']
                    
                    # 3. 获取活跃计时器
                    print("\n[3] 获取活跃计时器...")
                    active_response = requests.get(f"{BASE_URL}/timer/active")
                    if active_response.status_code == 200:
                        active_timers = active_response.json()
                        print(f"✓ 找到 {len(active_timers)} 个活跃计时器")
                        
                        for t in active_timers:
                            print(f"  - ID: {t['id']}, Plan: {t.get('planTitle', 'N/A')}, Elapsed: {t['elapsed']}s")
                    
                    # 4. 启动计时器
                    print("\n[4] 启动计时器...")
                    start_response = requests.post(f"{BASE_URL}/timer/{timer_id}/start")
                    if start_response.status_code == 200:
                        print(f"✓ 计时器启动成功")
                    
                    # 5. 删除计时器
                    print("\n[5] 删除计时器...")
                    delete_response = requests.delete(f"{BASE_URL}/timer/{timer_id}")
                    if delete_response.status_code == 200:
                        print(f"✓ 计时器删除成功")
                    
                else:
                    print(f"✗ 创建计时器失败: {create_response.status_code}")
                    print(f"  响应: {create_response.text}")
            else:
                print("⚠ 没有可用计划，请先创建计划")
        else:
            print(f"✗ 获取计划失败: {response.status_code}")
            print(f"  响应: {response.text}")
    
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    # 6. 创建自由计时器
    print("\n[6] 创建自由计时器...")
    try:
        create_response = requests.post(
            f"{BASE_URL}/timer/create",
            json={
                "plan_id": None,
                "title": "测试自由计时"
            }
        )
        
        if create_response.status_code == 201:
            timer = create_response.json()
            print(f"✓ 自由计时器创建成功")
            print(f"  Timer ID: {timer['id']}")
            print(f"  Title: {timer.get('title')}")
            
            # 清理
            requests.delete(f"{BASE_URL}/timer/{timer['id']}")
        else:
            print(f"✗ 创建自由计时器失败: {create_response.status_code}")
            print(f"  响应: {create_response.text}")
    
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_timer_api()
