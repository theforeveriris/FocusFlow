<template>
  <ErrorBoundary>
    <div class="space-y-6 animate-fade-in-up">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">时间追踪可视化</h1>
          <p class="text-gray-500 mt-1">查看你的时间分配日历</p>
        </div>
        
        <!-- Date Navigation -->
        <div class="flex items-center gap-4">
          <button
            @click="previousDay"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>
          
          <div class="flex items-center gap-2">
            <input
              v-model="selectedDate"
              type="date"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            <button
              @click="goToToday"
              class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
            >
              今天
            </button>
          </div>
          
          <button
            @click="nextDay"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
        </div>
      </div>
      
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <BaseCard class="text-center">
          <Clock class="w-6 h-6 text-primary-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ formatDuration(daySummary.total_duration) }}
          </div>
          <div class="text-sm text-gray-500">总时长</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <Target class="w-6 h-6 text-green-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ daySummary.session_count }}
          </div>
          <div class="text-sm text-gray-500">计时次数</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <TrendingUp class="w-6 h-6 text-orange-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ safeToFixed(daySummary.avg_focus_score) }}
          </div>
          <div class="text-sm text-gray-500">平均专注度</div>
        </BaseCard>
        
        <BaseCard class="text-center">
          <FolderKanban class="w-6 h-6 text-blue-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">
            {{ daySummary.plan_count }}
          </div>
          <div class="text-sm text-gray-500">关联计划</div>
        </BaseCard>
      </div>
      
      <!-- Timeline Calendar -->
      <BaseCard>
        <template #header>
          <h2 class="text-lg font-semibold text-gray-900">
            {{ formatDateHeader(selectedDate) }}
          </h2>
        </template>
        
        <div class="relative">
          <!-- Time Grid -->
          <div class="flex">
            <!-- Time Labels -->
            <div class="w-16 flex-shrink-0">
              <div
                v-for="hour in 24"
                :key="hour"
                class="h-12 border-b border-gray-100 text-xs text-gray-500 pr-2 text-right pt-1"
              >
                {{ formatHour(hour - 1) }}
              </div>
            </div>
            
            <!-- Timeline -->
            <div class="flex-1 relative">
              <!-- Grid Lines -->
              <div
                v-for="hour in 24"
                :key="hour"
                class="h-12 border-b border-gray-100"
              ></div>
              
              <!-- Time Blocks -->
              <div
                v-for="session in sessions"
                :key="session.id"
                :style="getSessionStyle(session)"
                class="absolute left-0 right-0 rounded-lg shadow-sm border-l-4 px-3 py-2 cursor-pointer hover:shadow-md transition-shadow overflow-hidden"
                @click="showSessionDetail(session)"
              >
                <div class="text-sm font-medium text-gray-900 truncate">
                  {{ session.plan_name || '自由计时' }}
                </div>
                <div class="text-xs text-gray-600 truncate">
                  {{ formatSessionTime(session) }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ formatDuration(session.duration) }}
                </div>
              </div>
              
              <!-- Current Time Indicator -->
              <div
                v-if="isToday"
                :style="getCurrentTimeStyle()"
                class="absolute left-0 right-0 h-0.5 bg-red-500 z-10"
              >
                <div class="absolute -left-2 -top-2 w-4 h-4 bg-red-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </BaseCard>
      
      <!-- Session Detail Modal -->
      <BaseModal v-model:show="showDetailModal" title="计时详情">
        <div v-if="selectedSession" class="space-y-4">
          <div>
            <label class="text-sm font-medium text-gray-700">计划</label>
            <p class="mt-1 text-gray-900">{{ selectedSession.plan_name || '自由计时' }}</p>
          </div>
          
          <div>
            <label class="text-sm font-medium text-gray-700">项目</label>
            <p class="mt-1 text-gray-900">{{ selectedSession.project_name || '-' }}</p>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-gray-700">开始时间</label>
              <p class="mt-1 text-gray-900">{{ formatTime(selectedSession.start_time) }}</p>
            </div>
            
            <div>
              <label class="text-sm font-medium text-gray-700">结束时间</label>
              <p class="mt-1 text-gray-900">{{ formatTime(selectedSession.end_time) }}</p>
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-gray-700">时长</label>
              <p class="mt-1 text-gray-900">{{ formatDuration(selectedSession.duration) }}</p>
            </div>
            
            <div>
              <label class="text-sm font-medium text-gray-700">专注度</label>
              <p class="mt-1 text-gray-900">{{ safeToFixed(selectedSession.focus_score) }}</p>
            </div>
          </div>
          
          <div v-if="selectedSession.notes">
            <label class="text-sm font-medium text-gray-700">备注</label>
            <p class="mt-1 text-gray-900">{{ selectedSession.notes }}</p>
          </div>
        </div>
      </BaseModal>
    </div>
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { 
  Clock, Target, TrendingUp, FolderKanban,
  ChevronLeft, ChevronRight
} from 'lucide-vue-next'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import ErrorBoundary from '@/components/common/ErrorBoundary.vue'
import { formatDuration, safeToFixed } from '@/utils/helpers'
import { handleApiError } from '@/utils/errorHandler'

interface TimerSession {
  id: number
  plan_id?: number
  plan_name?: string
  project_id?: number
  project_name?: string
  start_time: string
  end_time: string
  duration: number
  focus_score?: number
  notes?: string
}

interface DaySummary {
  total_duration: number
  session_count: number
  avg_focus_score: number
  plan_count: number
}

// State
const selectedDate = ref(new Date().toISOString().split('T')[0])
const sessions = ref<TimerSession[]>([])
const daySummary = ref<DaySummary>({
  total_duration: 0,
  session_count: 0,
  avg_focus_score: 0,
  plan_count: 0
})

const showDetailModal = ref(false)
const selectedSession = ref<TimerSession | null>(null)

// Computed
const isToday = computed(() => {
  return selectedDate.value === new Date().toISOString().split('T')[0]
})

// Methods
const formatDateHeader = (dateStr: string) => {
  const date = new Date(dateStr)
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${weekdays[date.getDay()]}`
}

const formatHour = (hour: number) => {
  return `${hour.toString().padStart(2, '0')}:00`
}

const formatTime = (datetime: string) => {
  const date = new Date(datetime)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const formatSessionTime = (session: TimerSession) => {
  return `${formatTime(session.start_time)} - ${formatTime(session.end_time)}`
}

const getSessionStyle = (session: TimerSession) => {
  const start = new Date(session.start_time)
  const end = new Date(session.end_time)
  
  const startMinutes = start.getHours() * 60 + start.getMinutes()
  const endMinutes = end.getHours() * 60 + end.getMinutes()
  
  const top = (startMinutes / 60) * 48 // 48px per hour
  const height = ((endMinutes - startMinutes) / 60) * 48
  
  // 根据专注度设置颜色
  let bgColor = '#e5e7eb' // 默认灰色
  let borderColor = '#9ca3af'
  
  if (session.focus_score !== undefined) {
    if (session.focus_score >= 80) {
      bgColor = '#dcfce7' // 绿色
      borderColor = '#22c55e'
    } else if (session.focus_score >= 60) {
      bgColor = '#dbeafe' // 蓝色
      borderColor = '#3b82f6'
    } else if (session.focus_score >= 40) {
      bgColor = '#fef3c7' // 黄色
      borderColor = '#f59e0b'
    } else {
      bgColor = '#fee2e2' // 红色
      borderColor = '#ef4444'
    }
  }
  
  return {
    top: `${top}px`,
    height: `${Math.max(height, 24)}px`,
    backgroundColor: bgColor,
    borderLeftColor: borderColor
  }
}

const getCurrentTimeStyle = () => {
  const now = new Date()
  const minutes = now.getHours() * 60 + now.getMinutes()
  const top = (minutes / 60) * 48
  
  return {
    top: `${top}px`
  }
}

const previousDay = () => {
  const date = new Date(selectedDate.value)
  date.setDate(date.getDate() - 1)
  selectedDate.value = date.toISOString().split('T')[0]
}

const nextDay = () => {
  const date = new Date(selectedDate.value)
  date.setDate(date.getDate() + 1)
  selectedDate.value = date.toISOString().split('T')[0]
}

const goToToday = () => {
  selectedDate.value = new Date().toISOString().split('T')[0]
}

const showSessionDetail = (session: TimerSession) => {
  selectedSession.value = session
  showDetailModal.value = true
}

const loadDayData = async () => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/timer/sessions?date=${selectedDate.value}`
    )
    
    if (response.ok) {
      const data = await response.json()
      sessions.value = data
      
      // 计算汇总数据
      daySummary.value = {
        total_duration: data.reduce((sum: number, s: TimerSession) => sum + s.duration, 0),
        session_count: data.length,
        avg_focus_score: data.length > 0
          ? data.reduce((sum: number, s: TimerSession) => sum + (s.focus_score || 0), 0) / data.length
          : 0,
        plan_count: new Set(data.filter((s: TimerSession) => s.plan_id).map((s: TimerSession) => s.plan_id)).size
      }
    }
  } catch (error) {
    handleApiError(error, '加载时间追踪数据')
  }
}

// Watch
watch(selectedDate, () => {
  loadDayData()
})

// Lifecycle
onMounted(() => {
  loadDayData()
})
</script>
