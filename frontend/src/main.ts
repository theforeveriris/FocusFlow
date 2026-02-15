import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'
import { setupGlobalErrorRecovery, logError } from './utils/errorHandler'

const app = createApp(App)

// 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误捕获:', err)
  console.error('错误信息:', info)
  
  // 记录错误日志
  logError(err, '全局错误', { info, componentName: instance?.$options?.name })
  
  // 显示友好的错误提示
  const errorMessage = err instanceof Error ? err.message : String(err)
  
  // 不自动刷新，让 ErrorBoundary 处理
  console.error(`页面出现错误：${errorMessage}`)
  
  // 阻止错误继续传播到控制台（已经记录了）
  return false
}

// 全局警告处理（开发环境）
if (import.meta.env.DEV) {
  app.config.warnHandler = (msg, instance, trace) => {
    console.warn('Vue 警告:', msg)
    console.warn('追踪:', trace)
  }
}

// 捕获未处理的 Promise 错误
window.addEventListener('unhandledrejection', (event) => {
  console.error('未处理的 Promise 错误:', event.reason)
  
  logError(event.reason, '未处理的 Promise 错误')
  
  // 如果是网络错误，提示用户
  const errorMessage = event.reason?.message || String(event.reason)
  if (errorMessage.includes('fetch') || errorMessage.includes('network') || errorMessage.includes('Failed to fetch')) {
    alert('网络请求失败，请检查：\n1. 后端服务是否运行\n2. 网络连接是否正常')
  }
  
  event.preventDefault()
})

// 捕获全局错误
window.addEventListener('error', (event) => {
  console.error('全局错误:', event.error)
  
  logError(event.error, '全局错误', {
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno
  })
  
  event.preventDefault()
})

// 设置全局错误恢复机制
setupGlobalErrorRecovery()

app.use(createPinia())
app.use(router)

app.mount('#app')
