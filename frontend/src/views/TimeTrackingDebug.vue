<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">时间追踪调试</h1>
    
    <div class="space-y-4">
      <!-- 计划列表 -->
      <div class="bg-white p-4 rounded-lg border">
        <h2 class="font-semibold mb-2">可用计划 ({{ availablePlans.length }})</h2>
        <div v-if="availablePlans.length === 0" class="text-gray-500">
          没有可用计划
        </div>
        <ul v-else class="space-y-2">
          <li v-for="plan in availablePlans" :key="plan.id" class="flex items-center gap-2">
            <span class="font-mono text-sm">ID: {{ plan.id }}</span>
            <span>{{ plan.title }}</span>
            <span class="text-xs text-gray-500">({{ plan.status }})</span>
          </li>
        </ul>
      </div>
      
      <!-- 测试表单 -->
      <div class="bg-white p-4 rounded-lg border">
        <h2 class="font-semibold mb-2">创建计时器</h2>
        <form @submit.prevent="createTimer" class="space-y-3">
          <div>
            <label class="block text-sm mb-1">选择计划</label>
            <select v-model="selectedPlanId" class="w-full border p-2 rounded">
              <option :value="null">不绑定计划</option>
              <option v-for="plan in availablePlans" :key="plan.id" :value="plan.id">
                {{ plan.title }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">当前选择: {{ selectedPlanId || '无' }}</p>
          </div>
          
          <div v-if="!selectedPlanId">
            <label class="block text-sm mb-1">计时器名称</label>
            <input v-model="timerTitle" type="text" class="w-full border p-2 rounded" />
          </div>
          
          <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
            创建计时器
          </button>
        </form>
      </div>
      
      <!-- 活跃计时器 -->
      <div class="bg-white p-4 rounded-lg border">
        <h2 class="font-semibold mb-2">活跃计时器 ({{ activeTimers.length }})</h2>
        <div v-if="activeTimers.length === 0" class="text-gray-500">
          没有活跃计时器
        </div>
        <ul v-else class="space-y-2">
          <li v-for="timer in activeTimers" :key="timer.id" class="border-b pb-2">
            <div class="font-medium">{{ timer.planTitle || timer.title || '未命名' }}</div>
            <div class="text-sm text-gray-500">
              ID: {{ timer.id }} | Plan ID: {{ timer.planId || '无' }} | Elapsed: {{ timer.elapsed }}s
            </div>
            <button
              @click="deleteTimer(timer.id)"
              class="text-xs text-red-500 hover:underline mt-1"
            >
              删除
            </button>
          </li>
        </ul>
      </div>
      
      <!-- 日志 -->
      <div class="bg-gray-100 p-4 rounded-lg">
        <h2 class="font-semibold mb-2">日志</h2>
        <pre class="text-xs overflow-auto max-h-60">{{ logs.join('\n') }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const availablePlans = ref<any[]>([])
const activeTimers = ref<any[]>([])
const selectedPlanId = ref<number | null>(null)
const timerTitle = ref('')
const logs = ref<string[]>([])

const log = (message: string) => {
  const timestamp = new Date().toLocaleTimeString()
  logs.value.push(`[${timestamp}] ${message}`)
  console.log(message)
}

onMounted(async () => {
  await loadPlans()
  await loadActiveTimers()
})

const loadPlans = async () => {
  try {
    log('正在获取计划列表...')
    const response = await fetch('http://localhost:8000/api/v1/plans?exclude_completed=true')
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    const plans = await response.json()
    availablePlans.value = plans.filter((p: any) => 
      p.status === 'todo' || p.status === 'in_progress'
    )
    
    log(`✓ 获取到 ${availablePlans.value.length} 个计划`)
  } catch (error) {
    log(`✗ 获取计划失败: ${error}`)
  }
}

const loadActiveTimers = async () => {
  try {
    log('正在获取活跃计时器...')
    const response = await fetch('http://localhost:8000/api/v1/timer/active')
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    activeTimers.value = await response.json()
    log(`✓ 获取到 ${activeTimers.value.length} 个活跃计时器`)
  } catch (error) {
    log(`✗ 获取活跃计时器失败: ${error}`)
  }
}

const createTimer = async () => {
  try {
    const payload = {
      plan_id: selectedPlanId.value,
      title: timerTitle.value || null
    }
    
    log(`正在创建计时器: ${JSON.stringify(payload)}`)
    
    const response = await fetch('http://localhost:8000/api/v1/timer/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
    
    const result = await response.json()
    log(`✓ 计时器创建成功: ID=${result.id}, PlanID=${result.planId}`)
    
    await loadActiveTimers()
    
    // 重置表单
    selectedPlanId.value = null
    timerTitle.value = ''
  } catch (error) {
    log(`✗ 创建计时器失败: ${error}`)
  }
}

const deleteTimer = async (timerId: number) => {
  try {
    log(`正在删除计时器 ${timerId}...`)
    const response = await fetch(`http://localhost:8000/api/v1/timer/${timerId}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    log(`✓ 计时器 ${timerId} 删除成功`)
    await loadActiveTimers()
  } catch (error) {
    log(`✗ 删除计时器失败: ${error}`)
  }
}
</script>
