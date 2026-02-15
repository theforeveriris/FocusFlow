/**
 * 全局错误处理工具
 */

export interface ErrorHandlerOptions {
  showAlert?: boolean
  logToConsole?: boolean
  redirectOnError?: string
  retryable?: boolean
}

/**
 * 处理 API 错误
 */
export function handleApiError(
  error: any,
  context: string = '操作',
  options: ErrorHandlerOptions = {}
): string {
  const {
    showAlert = true,
    logToConsole = true,
    redirectOnError,
    retryable = false
  } = options

  let errorMessage = `${context}失败`

  // 解析错误类型
  if (error.response) {
    // HTTP 错误响应
    const status = error.response.status
    const data = error.response.data

    switch (status) {
      case 400:
        errorMessage = `${context}失败：请求参数错误`
        break
      case 401:
        errorMessage = `${context}失败：未授权，请重新登录`
        break
      case 403:
        errorMessage = `${context}失败：没有权限`
        break
      case 404:
        errorMessage = `${context}失败：资源不存在`
        break
      case 500:
        errorMessage = `${context}失败：服务器错误`
        break
      default:
        errorMessage = `${context}失败：${data?.detail || data?.message || '未知错误'}`
    }
  } else if (error.request) {
    // 请求已发送但没有收到响应
    errorMessage = `${context}失败：网络连接失败，请检查后端服务是否运行`
  } else if (error.message) {
    // 其他错误
    errorMessage = `${context}失败：${error.message}`
  }

  // 记录到控制台
  if (logToConsole) {
    console.error(`[错误] ${context}:`, error)
  }

  // 显示警告框
  if (showAlert) {
    let alertMessage = errorMessage
    if (retryable) {
      alertMessage += '\n\n点击确定重试'
    }
    alert(alertMessage)
  }

  // 重定向
  if (redirectOnError) {
    setTimeout(() => {
      window.location.href = redirectOnError
    }, 1000)
  }

  return errorMessage
}

/**
 * 处理组件错误
 */
export function handleComponentError(
  error: any,
  componentName: string = '组件'
): void {
  console.error(`[${componentName}错误]:`, error)
  
  // 显示友好的错误提示
  const errorMessage = error instanceof Error ? error.message : String(error)
  console.error(`${componentName}渲染失败: ${errorMessage}`)
}

/**
 * 安全执行异步函数
 */
export async function safeAsync<T>(
  fn: () => Promise<T>,
  context: string = '操作',
  options: ErrorHandlerOptions = {}
): Promise<T | null> {
  try {
    return await fn()
  } catch (error) {
    handleApiError(error, context, options)
    return null
  }
}

/**
 * 重试函数
 */
export async function retryAsync<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: any

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error
      console.warn(`尝试 ${i + 1}/${maxRetries} 失败:`, error)
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError
}

/**
 * 检查网络连接
 */
export function checkNetworkConnection(): boolean {
  if (!navigator.onLine) {
    alert('网络连接已断开，请检查网络设置')
    return false
  }
  return true
}

/**
 * 检查后端服务
 */
export async function checkBackendService(baseUrl: string = 'http://localhost:8000'): Promise<boolean> {
  try {
    const response = await fetch(`${baseUrl}/docs`, { method: 'HEAD' })
    return response.ok
  } catch (error) {
    console.error('后端服务检查失败:', error)
    return false
  }
}

/**
 * 全局错误恢复
 */
export function setupGlobalErrorRecovery(): void {
  // 监听网络状态变化
  window.addEventListener('online', () => {
    console.log('网络已恢复')
    // 可以在这里重新加载数据
  })

  window.addEventListener('offline', () => {
    console.warn('网络已断开')
    alert('网络连接已断开，部分功能可能无法使用')
  })

  // 定期检查后端服务
  let backendCheckInterval: number | null = null
  
  const startBackendCheck = () => {
    backendCheckInterval = window.setInterval(async () => {
      const isBackendUp = await checkBackendService()
      if (!isBackendUp) {
        console.warn('后端服务不可用')
      }
    }, 30000) // 每30秒检查一次
  }

  const stopBackendCheck = () => {
    if (backendCheckInterval) {
      clearInterval(backendCheckInterval)
      backendCheckInterval = null
    }
  }

  // 页面可见时开始检查
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopBackendCheck()
    } else {
      startBackendCheck()
    }
  })

  // 初始启动检查
  if (!document.hidden) {
    startBackendCheck()
  }
}

/**
 * 创建错误日志
 */
export function logError(
  error: any,
  context: string,
  additionalInfo?: Record<string, any>
): void {
  const errorLog = {
    timestamp: new Date().toISOString(),
    context,
    error: error instanceof Error ? {
      message: error.message,
      stack: error.stack,
      name: error.name
    } : error,
    additionalInfo,
    userAgent: navigator.userAgent,
    url: window.location.href
  }

  console.error('[错误日志]', errorLog)

  // 可以在这里发送到错误追踪服务
  // sendToErrorTracking(errorLog)
}
