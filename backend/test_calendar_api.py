"""
测试时间追踪日历 API
"""
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api/v1/timer"

def test_sessions_by_date():
    """测试按日期查询计时会话"""
    print("\n=== 测试按日期查询计时会话 ===")
    
    # 测试今天
    today = date.today()
    response = requests.get(
        f"{BASE_URL}/sessions",
        params={"date": str(today)}
    )
    
    print(f"今天 ({today}):")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"会话数量: {len(data)}")
        
        if data:
            print("\n会话列表:")
            for session in data:
                print(f"  - {session.get('plan_title', '自由计时')}")
                print(f"    开始: {session['start_time']}")
                print(f"    结束: {session['end_time']}")
                print(f"    时长: {session['duration']}秒")
                print(f"    专注度: {session.get('focus_score', 'N/A')}")
                print()
    else:
        print(f"错误: {response.text}")
    
    # 测试昨天
    yesterday = today - timedelta(days=1)
    response = requests.get(
        f"{BASE_URL}/sessions",
        params={"date": str(yesterday)}
    )
    
    print(f"\n昨天 ({yesterday}):")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"会话数量: {len(data)}")
    else:
        print(f"错误: {response.text}")

def test_all_sessions():
    """测试查询所有会话"""
    print("\n=== 测试查询所有会话 ===")
    
    response = requests.get(f"{BASE_URL}/sessions")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"总会话数量: {len(data)}")
        
        if data:
            print("\n最近的会话:")
            for session in data[:3]:
                print(f"  - {session.get('plan_title', '自由计时')}")
                print(f"    时间: {session['start_time']}")
                print(f"    时长: {session['duration']}秒")
                print()
    else:
        print(f"错误: {response.text}")

if __name__ == "__main__":
    print("开始测试时间追踪日历 API...")
    print("=" * 50)
    
    try:
        test_sessions_by_date()
        test_all_sessions()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("\n错误: 无法连接到后端服务")
        print("请确保后端服务正在运行: http://localhost:8000")
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
