<template>
  <div class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">专注计时</h1>
        <p class="text-gray-500 mt-1">保持专注，提升效率</p>
      </div>
      
      <!-- Zen Mode Button -->
      <BaseButton variant="outline" @click="enterZenMode">
        <Maximize2 class="w-4 h-4" />
        Zen模式
      </BaseButton>
    </div>
    
    <!-- Timer Display -->
    <div class="bg-white rounded-2xl border border-gray-200 p-12 text-center">
      <!-- Flip Clock Display -->
      <div class="flex items-center justify-center gap-4 mb-8">
        <div class="flip-clock">
          <div class="text-8xl font-mono font-bold text-gray-900 tracking-wider">
            {{ formattedTime }}
          </div>
        </div>
      </div>
      
      <!-- Hitokoto Quote -->
      <div class="mb-8 text-gray-500 italic">
        "{{ currentQuote }}"
      </div>
      
      <!-- Controls -->
      <div class="flex items-center justify-center gap-4">
        <BaseButton
          v-if="canStart"
          size="lg"
          @click="startTimer"
        >
          <Play class="w-5 h-5" />
          开始专注
        </BaseButton>
        
        <template v-else>
          <BaseButton
            v-if="canPause"
            variant="secondary"
            size="lg"
            @click="pauseTimer"
          >
            <Pause class="w-5 h-5" />
            暂停
          </BaseButton>
          
          <BaseButton
            v-if="isPaused"
            size="lg"
            @click="resumeTimer"
          >
            <Play class="w-5 h-5" />
            继续
          </BaseButton>
          
          <BaseButton
            v-if="canStop"
            variant="danger"
            size="lg"
            @click="stopTimer"
          >
            <Square class="w-5 h-5" />
            结束
          </BaseButton>
        </template>
      </div>
      
      <!-- Timer Presets -->
      <div class="mt-8 flex items-center justify-center gap-2">
        <button
          v-for="preset in timerPresets"
          :key="preset"
          @click="setPreset(preset)
          "
          class="px-4 py-2 rounded-lg border border-gray-200 text-sm text-gray-600 hover:bg-gray-50 transition-colors"
          :class="{ 'bg-primary-50 border-primary-500 text-primary-600': selectedPreset === preset }"
        >
          {{ preset }}分钟
        </button>
      </div>
    </div>
    
    <!-- Today's Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <BaseCard class="text-center">
        <Clock class="w-8 h-8 text-primary-500 mx-auto mb-2" />
        <div class="text-2xl font-bold text-gray-900">
          {{ formatDuration(todayStats.total_duration) }}
        </div>
        <div class="text-sm text-gray-500">今日专注时长</div>
      </BaseCard>
      
      <BaseCard class="text-center">
        <Target class="w-8 h-8 text-green-500 mx-auto mb-2" />
        <div class="text-2xl font-bold text-gray-900">
          {{ todayStats.session_count }}
        </div>
        <div class="text-sm text-gray-500">专注次数</div>
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
    <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-900">最近记录</h3>
      </div>
      <div class="divide-y divide-gray-200">
        <div
          v-for="session in sessions.slice(0, 5)"
          :key="session.id"
          class="px-6 py-4 flex items-center justify-between hover:bg-gray-50"
        >
          <div>
            <div class="font-medium text-gray-900">
              {{ session.plan_title || session.project_name || '自由专注' }}
            </div>
            <div class="text-sm text-gray-500">
              {{ formatDateTime(session.start_time) }}
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
        
        <div v-if="sessions.length === 0" class="px-6 py-8 text-center text-gray-500">
          暂无专注记录
        </div>
      </div>
    </div>
    
    <!-- Zen Mode Overlay -->
    <ZenMode
      v-model="isZenMode"
      :time="formattedTime"
      :quote="currentQuote"
      @stop="stopTimer"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useTimerStore } from '@/stores/timerStore'
import { 
  Play, Pause, Square, Maximize2, 
  Clock, Target, TrendingUp 
} from 'lucide-vue-next'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import ZenMode from '@/components/timer/ZenMode.vue'
import { formatDuration, formatDateTime, safeToFixed } from '@/utils/helpers'

const timerStore = useTimerStore()

// State
const isZenMode = ref(false)
const selectedPreset = ref<number | null>(null)
const currentQuote = ref('专注当下，成就未来。')

const timerPresets = [15, 25, 45, 60]

// Quotes
const quotes = [
  '专注当下，成就未来。',
  '每一次专注，都是对自己的投资。',
  '保持专注，让时间更有价值。',
  '深度工作，创造卓越。',
  '专注是一种选择，也是一种能力。',
  '今天的专注，明天的收获。'
]

// Computed
const formattedTime = computed(() => timerStore.formattedTime)
const isRunning = computed(() => timerStore.isRunning)
const isPaused = computed(() => timerStore.isPaused)
const canStart = computed(() => timerStore.canStart)
const canPause = computed(() => timerStore.canPause)
const canStop = computed(() => timerStore.canStop)
const todayStats = computed(() => timerStore.todayStats)
const sessions = computed(() => timerStore.sessions)

// Methods
onMounted(() => {
  timerStore.checkRunningSession()
  timerStore.fetchTodayStats()
  timerStore.fetchSessions()
  
  // Random quote
  currentQuote.value = quotes[Math.floor(Math.random() * quotes.length)]
})

onUnmounted(() => {
  // Cleanup if needed
})

const startTimer = async () => {
  await timerStore.startTimer({})
}

const pauseTimer = async () => {
  await timerStore.pauseTimer()
}

const resumeTimer = () => {
  // Resume is same as start for now
  isPaused.value = false
  timerStore.isPaused = false
  timerStore.startTimerInterval()
}

const stopTimer = async () => {
  await timerStore.stopTimer()
  isZenMode.value = false
  await timerStore.fetchTodayStats()
  await timerStore.fetchSessions()
}

const enterZenMode = () => {
  if (!isRunning.value) {
    startTimer()
  }
  isZenMode.value = true
}

const setPreset = (minutes: number) => {
  selectedPreset.value = minutes
  // TODO: Implement countdown timer with preset
}
</script>
