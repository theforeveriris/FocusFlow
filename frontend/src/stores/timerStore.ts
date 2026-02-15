import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { timerApi } from '@/api/timer'
import type { TimerSession, TimerTodayStats } from '@/types'

export const useTimerStore = defineStore('timer', () => {
  // State
  const sessions = ref<TimerSession[]>([])
  const currentSession = ref<TimerSession | null>(null)
  const todayStats = ref<TimerTodayStats>({
    total_duration: 0,
    session_count: 0
  })
  const elapsedSeconds = ref(0)
  const isRunning = ref(false)
  const isPaused = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  let timerInterval: ReturnType<typeof setInterval> | null = null

  // Getters
  const formattedTime = computed(() => {
    const hours = Math.floor(elapsedSeconds.value / 3600)
    const minutes = Math.floor((elapsedSeconds.value % 3600) / 60)
    const seconds = elapsedSeconds.value % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  })

  const canStart = computed(() => !isRunning.value && !isPaused.value)
  const canPause = computed(() => isRunning.value && !isPaused.value)
  const canStop = computed(() => isRunning.value || isPaused.value)

  // Actions
  const fetchSessions = async (params?: { plan_id?: number; project_id?: number }) => {
    loading.value = true
    try {
      const response = await timerApi.getSessions(params)
      sessions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch sessions'
    } finally {
      loading.value = false
    }
  }

  const fetchTodayStats = async () => {
    try {
      const response = await timerApi.getTodayStats()
      todayStats.value = response.data
    } catch (err: any) {
      console.error('Failed to fetch today stats:', err)
    }
  }

  const checkRunningSession = async () => {
    try {
      const response = await timerApi.getRunningSession()
      if (response.data) {
        currentSession.value = response.data
        const startTime = new Date(response.data.start_time).getTime()
        const now = new Date().getTime()
        elapsedSeconds.value = Math.floor((now - startTime) / 1000)
        isRunning.value = true
        startTimerInterval()
      }
    } catch (err) {
      console.error('Failed to check running session:', err)
    }
  }

  const startTimer = async (data: { plan_id?: number; project_id?: number; is_zen_mode?: boolean }) => {
    loading.value = true
    error.value = null
    try {
      const response = await timerApi.start(data)
      currentSession.value = response.data
      elapsedSeconds.value = 0
      isRunning.value = true
      isPaused.value = false
      startTimerInterval()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to start timer'
      return null
    } finally {
      loading.value = false
    }
  }

  const pauseTimer = async () => {
    if (!currentSession.value) return
    loading.value = true
    try {
      await timerApi.pause(currentSession.value.id)
      isPaused.value = true
      stopTimerInterval()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to pause timer'
    } finally {
      loading.value = false
    }
  }

  const stopTimer = async (notes?: string) => {
    if (!currentSession.value) return
    loading.value = true
    try {
      const response = await timerApi.stop(currentSession.value.id, { notes })
      sessions.value.unshift(response.data)
      resetTimer()
      await fetchTodayStats()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to stop timer'
      return null
    } finally {
      loading.value = false
    }
  }

  const startTimerInterval = () => {
    timerInterval = setInterval(() => {
      elapsedSeconds.value++
    }, 1000)
  }

  const stopTimerInterval = () => {
    if (timerInterval) {
      clearInterval(timerInterval)
      timerInterval = null
    }
  }

  const resetTimer = () => {
    stopTimerInterval()
    currentSession.value = null
    elapsedSeconds.value = 0
    isRunning.value = false
    isPaused.value = false
  }

  return {
    sessions,
    currentSession,
    todayStats,
    elapsedSeconds,
    isRunning,
    isPaused,
    loading,
    error,
    formattedTime,
    canStart,
    canPause,
    canStop,
    fetchSessions,
    fetchTodayStats,
    checkRunningSession,
    startTimer,
    pauseTimer,
    stopTimer,
    resetTimer
  }
})
