<template>
  <div v-if="hasError" class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <div class="text-center">
        <!-- Error Icon -->
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
          <svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        
        <!-- Error Title -->
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          页面加载失败
        </h3>
        
        <!-- Error Message -->
        <p class="text-sm text-gray-500 mb-6">
          {{ errorMessage }}
        </p>
        
        <!-- Error Details (Collapsible) -->
        <details v-if="errorDetails" class="text-left mb-6">
          <summary class="cursor-pointer text-sm text-gray-600 hover:text-gray-900">
            查看详细错误信息
          </summary>
          <pre class="mt-2 p-3 bg-gray-100 rounded text-xs overflow-auto max-h-40">{{ errorDetails }}</pre>
        </details>
        
        <!-- Action Buttons -->
        <div class="flex flex-col gap-2">
          <button
            @click="retry"
            class="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
          >
            重试
          </button>
          
          <button
            @click="goHome"
            class="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            返回首页
          </button>
          
          <button
            @click="reload"
            class="w-full px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            刷新页面
          </button>
        </div>
        
        <!-- Help Text -->
        <p class="mt-6 text-xs text-gray-500">
          如果问题持续出现，请尝试：<br>
          1. 清除浏览器缓存（Ctrl + Shift + Delete）<br>
          2. 检查后端服务是否运行<br>
          3. 查看浏览器控制台错误信息（F12）
        </p>
      </div>
    </div>
  </div>
  
  <slot v-else></slot>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const hasError = ref(false)
const errorMessage = ref('发生了一个未知错误')
const errorDetails = ref('')

onErrorCaptured((err, instance, info) => {
  console.error('ErrorBoundary 捕获错误:', err)
  console.error('错误信息:', info)
  
  hasError.value = true
  errorMessage.value = err instanceof Error ? err.message : String(err)
  errorDetails.value = `${err}\n\n组件信息: ${info}\n\n堆栈: ${err instanceof Error ? err.stack : ''}`
  
  // 阻止错误继续传播
  return false
})

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
  errorDetails.value = ''
  
  // 重新加载当前路由
  router.go(0)
}

const goHome = () => {
  hasError.value = false
  router.push('/')
}

const reload = () => {
  window.location.reload()
}
</script>
