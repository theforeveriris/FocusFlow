<template>
  <ErrorBoundary>
    <div v-if="isLoading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-gray-600">加载中...</p>
      </div>
    </div>
    
    <div v-else class="space-y-6 animate-fade-in-up">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">时间追踪</h1>
          <p class="text-gray-500 mt-1">记录和管理你的时间</p>
        </div>
        
        <BaseButton @click="showAddTimerModal = true">
          <Plus class="w-4 h-4" />
          添加计时器
        </BaseButton>
      </div>
      
      <!-- Active Timers -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <BaseCard
          v-for="timer in activeTimers"
          :key="timer.id"
          class="relative"
          :class="{ 'ring-2 ring-primary-500': timer.isRunning }"
        >
          <!-- Timer Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900">
                {{ timer.planTitle || '自由计时' }}
              </h3>
              <p v-if="timer.planDescription" class="text-sm text-gray-500 mt-1">
                {{ timer.planDescription }}
              </p>
            </div>
            <button
              @click="deleteTimer(timer.id)"
              class="p-1 text-gray-400 hover:text-red-500 transition-colors"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
          
          <!-- Timer Display -->
          <div class="text-center mb-4">
            <div class="text-4xl font-mono font-bold text-gray-900">
              {{ formatTimerDisplay(timer.elapsed) }}
            </div>
            <div v-if="timer.planId" class="text-xs text-gray-500 mt-1">
              绑定计划 #{{ timer.planId }}
            </div>
          </div>
          
          <!-- Timer Controls -->
          <div class="flex items-center justify-center gap-2">
            <BaseButton
              v-if="!timer.isRunning"
              size="sm"
              @click="startTimer(timer.id)"
            >
              <Play class="w-4 h-4" />
              开始
            </BaseButton>
            
            <BaseButton
              v-else
              variant="secondary"
              size="sm"
              @click="pauseTimer(timer.id)"
            >
              <Pause class="w-4 h-4" />
              暂停
            </BaseButton>
            
            <BaseButton
              v-if="timer.elapsed > 0"
              variant="danger"
              size="sm"
              @click="stopTimer(timer.id)"
            >
              <Square class="w-4 h-4" />
              结束
            </BaseButton>
          </div>
          
          <!-- Running Indicator -->
          <div
            v-if="timer.isRunning"
            class="absolute top-2 right-2 w-3 h-3 bg-green-500 rounded-full animate-pulse"
          ></div>
        </BaseCard>
        
        <!-- Add Timer Card -->
        <button
          @click="showAddTimerModal = true"
          class="border-2 border-dashed border-gray-300 rounded-xl p-8 flex flex-col items-center justify-center hover:border-primary-500 hover:bg-primary-50 transition-colors"
        >
          <Plus class="w-8 h-8 text-gray-400 mb-2" />
          <span class="text-gray-600">添加计时器</span>
        </button>
      </div>
      
      <!-- Today's Summary -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <BaseCard class="text-center">
          <Clock class="w-8 h-8 text-primary-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ formatDuration(todayStats.total_duration) }}
          </div>
          <div class="text-sm text-gray-500">今日总时长</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <Target class="w-8 h-8 text-green-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ todayStats.session_count }}
          </div>
          <div class="text-sm text-gray-500">完成次数</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <Timer class="w-8 h-8 text-blue-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ activeTimers.length }}
          </div>
          <div class="text-sm text-gray-500">活跃计时器</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <TrendingUp class="w-8 h-8 text-orange-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ safeToFixed(todayStats.focus_score_avg) }}
          </div>
          <div class="text-sm text-gray-500">平均专注度</div>
        </BaseCard>
      </div>
      
      <!-- Recent Sessions -->
      <BaseCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="font-semibold text-gray-900">最近记录</h3>
            <button
              @click="$router.push('/statistics')"
              class="text-sm text-primary-600 hover:text-primary-700"
            >
              查看全部 →
            </button>
          </div>
        </template>
        
        <div class="divide-y divide-gray-200">
          <div
            v-for="session in recentSessions"
            :key="session.id"
            class="py-4 flex items-center justify-between hover:bg-gray-50 -mx-4 px-4"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <Clock class="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">
                  {{ session.plan_title || '自由计时' }}
                </div>
                <div class="text-sm text-gray-500">
                  {{ formatDateTime(session.start_time) }}
                </div>
              </div>
            </div>
            
            <div class="text-right">
              <div class="font-medium text-gray-900">
                {{ formatDuration(session.duration) }}
              </div>
              <div class="text-sm text-gray-500">
                专注度: {{ safeToFixed(session.focus_score) }}
              </div>
            </div>
          </div>
          
          <div v-if="recentSessions.length === 0" class="py-8 text-center text-gray-500">
            暂无时间记录
          </div>
        </div>
      </BaseCard>
    </div>
    
    <!-- Add Timer Modal -->
    <BaseModal v-model="showAddTimerModal" title="添加计时器">
      <form @submit.prevent="addTimer" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            绑定计划（可选）
          </label>
          <select
            v-model="newTimer.planId"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option :value="null">自由计时（不绑定计划）</option>
            <option
              v-for="plan in availablePlans"
              :key="plan.id"
              :value="plan.id"
            >
              {{ plan.title }}
            </option>
          </select>
        </div>
        
        <div v-if="!newTimer.planId">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            计时器名称
          </label>
          <input
            v-model="newTimer.title"
            type="text"
            placeholder="例如：阅读、学习、工作..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
        
        <div class="flex justify-end gap-2">
          <BaseButton type="button" variant="outline" @click="showAddTimerModal = false">
            取消
          </BaseButton>
          <BaseButton type="submit" :loading="loading">
            添加
          </BaseButton>
        </div>
      </form>
    </BaseModal>
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Plus, Play, Pause, Square, Clock, Target, Timer,
  TrendingUp, Trash2
} from 'lucide-vue-next'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import ErrorBoundary from '@/components/common/ErrorBoundary.vue'
import { formatDuration, formatDateTime, formatTimerDisplay, safeToFixed } from '@/utils/helpers'
import { handleApiError } from '@/utils/errorHandler'

const router = useRouter()

// State
const isLoading = ref(true)
const loading = ref(false)
const showAddTimerModal = ref(false)
const activeTimers = ref<any[]>([])
const recentSessions = ref<any[]>([])
const availablePlans = ref<any[]>([])
const todayStats = ref({
  total_duration: 0,
  session_count: 0,
  focus_score_avg: null
})

const newTimer = ref({
  planId: null as number | null,
  title: ''
})

let intervalId: number | null = null

// Methods
onMounted(async () => {
  await loadData()
  startInterval()
})

onUnmounted(() => {
  stopInterval()
})

const loadData = async () => {
  isLoading.value = true
  try {
    console.log('Loading time tracking data...')
    await Promise.all([
      fetchActiveTimers(),
      fetchRecentSessions(),
      fetchAvailablePlans(),
      fetchTodayStats()
    ])
    console.log('Data loaded successfully')
    console.log('Available plans:', availablePlans.value)
  } catch (error) {
    handleApiError(error, '加载数据')
  } finally {
    isLoading.value = false
  }
}

const fetchActiveTimers = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/timer/active')
    if (!response.ok) throw new Error('Failed to fetch active timers')
    activeTimers.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch active timers:', error)
    activeTimers.value = []
  }
}

const fetchRecentSessions = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/timer/sessions?limit=10')
    if (!response.ok) throw new Error('Failed to fetch sessions')
    recentSessions.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch sessions:', error)
    recentSessions.value = []
  }
}

const fetchAvailablePlans = async () => {
  try {
    // 获取未完成的计划（todo 和 in_progress）
    const response = await fetch('http://localhost:8000/api/v1/plans?exclude_completed=true')
    if (!response.ok) throw new Error('Failed to fetch plans')
    const plans = await response.json()
    // 只显示未完成的计划
    availablePlans.value = plans.filter((p: any) => 
      p.status === 'todo' || p.status === 'in_progress'
    )
    console.log('Available plans:', availablePlans.value)
  } catch (error) {
    console.error('Failed to fetch plans:', error)
    availablePlans.value = []
  }
}

const fetchTodayStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/timer/stats/today')
    if (!response.ok) throw new Error('Failed to fetch stats')
    todayStats.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

const addTimer = async () => {
  loading.value = true
  try {
    const payload = {
      plan_id: newTimer.value.planId,
      title: newTimer.value.title
    }
    
    console.log('Creating timer with payload:', payload)
    
    const response = await fetch('http://localhost:8000/api/v1/timer/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      console.error('Failed to create timer:', errorData)
      throw new Error(errorData.detail || 'Failed to create timer')
    }
    
    const result = await response.json()
    console.log('Timer created:', result)
    
    await fetchActiveTimers()
    showAddTimerModal.value = false
    newTimer.value = { planId: null, title: '' }
  } catch (error) {
    handleApiError(error, '添加计时器')
  } finally {
    loading.value = false
  }
}

const startTimer = async (timerId: number) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/timer/${timerId}/start`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to start timer')
    await fetchActiveTimers()
  } catch (error) {
    handleApiError(error, '启动计时器')
  }
}

const pauseTimer = async (timerId: number) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/timer/${timerId}/pause`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to pause timer')
    await fetchActiveTimers()
  } catch (error) {
    handleApiError(error, '暂停计时器')
  }
}

const stopTimer = async (timerId: number) => {
  if (!confirm('确定要结束这个计时器吗？时间记录将被保存。')) return
  
  try {
    const response = await fetch(`http://localhost:8000/api/v1/timer/${timerId}/stop`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to stop timer')
    
    await Promise.all([
      fetchActiveTimers(),
      fetchRecentSessions(),
      fetchTodayStats()
    ])
  } catch (error) {
    handleApiError(error, '结束计时器')
  }
}

const deleteTimer = async (timerId: number) => {
  if (!confirm('确定要删除这个计时器吗？')) return
  
  try {
    const response = await fetch(`http://localhost:8000/api/v1/timer/${timerId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete timer')
    await fetchActiveTimers()
  } catch (error) {
    handleApiError(error, '删除计时器')
  }
}

const startInterval = () => {
  intervalId = window.setInterval(() => {
    // Update elapsed time for running timers
    activeTimers.value.forEach(timer => {
      if (timer.isRunning) {
        timer.elapsed += 1
      }
    })
  }, 1000)
}

const stopInterval = () => {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}
</script>
