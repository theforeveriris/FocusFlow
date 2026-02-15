import { format, parseISO, differenceInSeconds } from 'date-fns'
import { zhCN } from 'date-fns/locale'

// Format duration from seconds to readable string
export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}小时${minutes > 0 ? ` ${minutes}分` : ''}`
  } else if (minutes > 0) {
    return `${minutes}分${secs > 0 ? ` ${secs}秒` : ''}`
  } else {
    return `${secs}秒`
  }
}

// Format duration for timer display (HH:MM:SS)
export function formatTimerDisplay(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// Format date
export function formatDate(date: string | Date, formatStr: string = 'yyyy-MM-dd'): string {
  const d = typeof date === 'string' ? parseISO(date) : date
  return format(d, formatStr, { locale: zhCN })
}

// Format datetime
export function formatDateTime(date: string | Date): string {
  const d = typeof date === 'string' ? parseISO(date) : date
  return format(d, 'yyyy-MM-dd HH:mm', { locale: zhCN })
}

// Format currency
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(amount)
}

// Get priority matrix label
export function getPriorityLabel(priority: string): string {
  const labels: Record<string, string> = {
    'urgent_important': '紧急且重要',
    'not_urgent_important': '重要不紧急',
    'urgent_not_important': '紧急不重要',
    'not_urgent_not_important': '不紧急不重要'
  }
  return labels[priority] || priority
}

// Get priority matrix color
export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    'urgent_important': '#ef4444',
    'not_urgent_important': '#f59e0b',
    'urgent_not_important': '#3b82f6',
    'not_urgent_not_important': '#6b7280'
  }
  return colors[priority] || '#6b7280'
}

// Get status label
export function getStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    'todo': '待办',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return labels[status] || status
}

// Get status color
export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    'todo': '#6b7280',
    'in_progress': '#3b82f6',
    'completed': '#10b981',
    'cancelled': '#9ca3af'
  }
  return colors[status] || '#6b7280'
}

// Generate random color
export function generateRandomColor(): string {
  const colors = [
    '#3b82f6', '#ef4444', '#f59e0b', '#10b981',
    '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

// Debounce function
export function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// Throttle function
export function throttle<T extends (...args: any[]) => void>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// Local storage helpers
export const storage = {
  get: <T>(key: string, defaultValue: T): T => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch {
      return defaultValue
    }
  },
  set: (key: string, value: any): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (e) {
      console.error('Storage error:', e)
    }
  },
  remove: (key: string): void => {
    localStorage.removeItem(key)
  }
}

// Safely format number to fixed decimal places
export function safeToFixed(value: any, decimals: number = 1): string {
  // Handle number type
  if (typeof value === 'number' && !isNaN(value)) {
    return value.toFixed(decimals)
  }
  
  // Handle string type (try to parse)
  if (typeof value === 'string') {
    const num = parseFloat(value)
    if (!isNaN(num)) {
      return num.toFixed(decimals)
    }
  }
  
  // Handle null, undefined, or invalid values
  return '-'
}

// Safely format number with locale
export function safeFormatNumber(value: any, options?: Intl.NumberFormatOptions): string {
  if (typeof value === 'number' && !isNaN(value)) {
    return new Intl.NumberFormat('zh-CN', options).format(value)
  }
  
  if (typeof value === 'string') {
    const num = parseFloat(value)
    if (!isNaN(num)) {
      return new Intl.NumberFormat('zh-CN', options).format(num)
    }
  }
  
  return '-'
}
