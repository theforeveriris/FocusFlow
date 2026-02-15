"""
测试 API 性能和响应时间
"""
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(name, url):
    """测试单个端点"""
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✓ {name}: {elapsed:.3f}s - OK")
            return True, elapsed
        else:
            print(f"✗ {name}: {elapsed:.3f}s - Status {response.status_code}")
            return False, elapsed
    except Exception as e:
        print(f"✗ {name}: ERROR - {str(e)}")
        return False, 0

def main():
    print("=" * 60)
    print("API 性能测试")
    print("=" * 60)
    
    endpoints = [
        ("分类列表", f"{BASE_URL}/accounting/categories"),
        ("交易记录", f"{BASE_URL}/accounting/transactions"),
        ("财务汇总", f"{BASE_URL}/accounting/summary"),
        ("账户汇总", f"{BASE_URL}/accounts/summary"),
        ("账户列表", f"{BASE_URL}/accounts"),
    ]
    
    results = []
    for name, url in endpoints:
        success, elapsed = test_endpoint(name, url)
        results.append((name, success, elapsed))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    total_time = sum(r[2] for r in results)
    success_count = sum(1 for r in results if r[1])
    
    print(f"成功: {success_count}/{len(results)}")
    print(f"串行总时间: {total_time:.3f}s")
    print(f"并行预计时间: {max(r[2] for r in results):.3f}s")
    print(f"性能提升: {(total_time / max(r[2] for r in results)):.1f}x")
    
    print("\n建议:")
    if total_time > 2:
        print("⚠ 总响应时间较长，建议:")
        print("  1. 使用并行请求 (Promise.all)")
        print("  2. 添加数据库索引")
        print("  3. 启用查询缓存")
    else:
        print("✓ API 响应速度良好")

if __name__ == "__main__":
    main()
