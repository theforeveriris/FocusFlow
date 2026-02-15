"""
创建活跃计时器表
"""
import sqlite3

def create_active_timers_table():
    conn = sqlite3.connect('focusflow.db')
    cursor = conn.cursor()
    
    # 创建活跃计时器表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS active_timers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id INTEGER,
        title TEXT,
        elapsed INTEGER DEFAULT 0,
        is_running BOOLEAN DEFAULT 0,
        start_time TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plan_id) REFERENCES plans (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ 活跃计时器表创建成功")

if __name__ == "__main__":
    create_active_timers_table()
