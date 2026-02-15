from datetime import datetime, timedelta
from typing import Optional


def format_duration(seconds: int) -> str:
    """Format seconds to human readable string"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO string"""
    if dt:
        return dt.isoformat()
    return None


def get_start_of_day(dt: Optional[datetime] = None) -> datetime:
    """Get start of day"""
    if dt is None:
        dt = datetime.now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def get_start_of_week(dt: Optional[datetime] = None) -> datetime:
    """Get start of week (Monday)"""
    if dt is None:
        dt = datetime.now()
    return (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)


def get_start_of_month(dt: Optional[datetime] = None) -> datetime:
    """Get start of month"""
    if dt is None:
        dt = datetime.now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def priority_matrix_label(priority: str) -> str:
    """Get human readable priority label"""
    labels = {
        "urgent_important": "紧急且重要",
        "not_urgent_important": "重要不紧急",
        "urgent_not_important": "紧急不重要",
        "not_urgent_not_important": "不紧急不重要"
    }
    return labels.get(priority, priority)


def priority_matrix_color(priority: str) -> str:
    """Get priority matrix color"""
    colors = {
        "urgent_important": "#ef4444",
        "not_urgent_important": "#f59e0b",
        "urgent_not_important": "#3b82f6",
        "not_urgent_not_important": "#6b7280"
    }
    return colors.get(priority, "#6b7280")
