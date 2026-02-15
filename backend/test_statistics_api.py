"""
测试统计 API
"""
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api/v1/statistics"

def test_overview():
    """测试概览数据"""
    print("\n=== 测试概览数据 ===")
    
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1)
    
    response = requests.get(
        f"{BASE_URL}/overview",
        params={
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"总专注时长: {data['total_duration']}秒")
        print(f"专注次数: {data['session_count']}")
        print(f"平均专注度: {data['avg_focus_score']}")
        print(f"完成计划: {data['completed_plans']}/{data['total_plans']}")
        print(f"总收入: ¥{data['total_income']}")
        print(f"总支出: ¥{data['total_expense']}")
        print(f"净资产: ¥{data['net_worth']}")
    else:
        print(f"错误: {response.text}")

def test_time_trend():
    """测试时间趋势"""
    print("\n=== 测试时间趋势 ===")
    
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    response = requests.get(
        f"{BASE_URL}/time-trend",
        params={
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"数据点数量: {len(data)}")
        if data:
            print(f"示例数据: {data[0]}")
    else:
        print(f"错误: {response.text}")

def test_plan_completion():
    """测试计划完成率"""
    print("\n=== 测试计划完成率 ===")
    
    response = requests.get(f"{BASE_URL}/plan-completion")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"数据: {data}")
    else:
        print(f"错误: {response.text}")

def test_project_time():
    """测试项目时间分布"""
    print("\n=== 测试项目时间分布 ===")
    
    response = requests.get(f"{BASE_URL}/project-time")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"项目数量: {len(data)}")
        for item in data[:3]:
            print(f"  {item['name']}: {item['duration']}秒")
    else:
        print(f"错误: {response.text}")

def test_focus_trend():
    """测试专注度趋势"""
    print("\n=== 测试专注度趋势 ===")
    
    response = requests.get(f"{BASE_URL}/focus-trend")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"数据点数量: {len(data)}")
        if data:
            print(f"示例数据: {data[0]}")
    else:
        print(f"错误: {response.text}")

def test_heatmap():
    """测试热力图"""
    print("\n=== 测试热力图 ===")
    
    response = requests.get(f"{BASE_URL}/heatmap")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"数据点数量: {len(data)}")
        if data:
            print(f"示例数据: {data[0]}")
    else:
        print(f"错误: {response.text}")

def test_finance_trend():
    """测试收支趋势"""
    print("\n=== 测试收支趋势 ===")
    
    response = requests.get(f"{BASE_URL}/finance-trend")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"数据点数量: {len(data)}")
        if data:
            print(f"示例数据: {data[0]}")
    else:
        print(f"错误: {response.text}")

def test_expense_category():
    """测试支出分类"""
    print("\n=== 测试支出分类 ===")
    
    response = requests.get(f"{BASE_URL}/expense-category")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"分类数量: {len(data)}")
        for item in data[:3]:
            print(f"  {item['name']}: ¥{item['value']}")
    else:
        print(f"错误: {response.text}")

def test_daily_distribution():
    """测试每日时间分布"""
    print("\n=== 测试每日时间分布 ===")
    
    response = requests.get(f"{BASE_URL}/daily-distribution")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        print("每日时间分布:")
        for i, hours in enumerate(data):
            print(f"  {weekdays[i]}: {hours}小时")
    else:
        print(f"错误: {response.text}")

def test_priority_distribution():
    """测试优先级分布"""
    print("\n=== 测试优先级分布 ===")
    
    response = requests.get(f"{BASE_URL}/priority-distribution")
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        priorities = ['紧急且重要', '重要不紧急', '紧急不重要', '不紧急不重要']
        print("优先级分布:")
        for i, percentage in enumerate(data):
            print(f"  {priorities[i]}: {percentage}%")
    else:
        print(f"错误: {response.text}")

if __name__ == "__main__":
    print("开始测试统计 API...")
    print("=" * 50)
    
    try:
        test_overview()
        test_time_trend()
        test_plan_completion()
        test_project_time()
        test_focus_trend()
        test_heatmap()
        test_finance_trend()
        test_expense_category()
        test_daily_distribution()
        test_priority_distribution()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("\n错误: 无法连接到后端服务")
        print("请确保后端服务正在运行: http://localhost:8000")
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
