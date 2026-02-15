import api from './index'
import type { TimerSession, TimerTodayStats } from '@/types'

export interface TimerStartData {
  plan_id?: number
  project_id?: number
  is_zen_mode?: boolean
}

export interface TimerUpdateData {
  notes?: string
}

export const timerApi = {
  // Get all sessions
  getSessions: (params?: { plan_id?: number; project_id?: number }) =>
    api.get<TimerSession[]>('/timer/sessions', { params }),

  // Get today's stats
  getTodayStats: () =>
    api.get<TimerTodayStats>('/timer/today'),

  // Get running session
  getRunningSession: () =>
    api.get<TimerSession | null>('/timer/running'),

  // Start timer
  start: (data: TimerStartData) =>
    api.post<TimerSession>('/timer/start', data),

  // Pause timer
  pause: (sessionId: number) =>
    api.post<TimerSession>(`/timer/${sessionId}/pause`),

  // Stop timer
  stop: (sessionId: number, data?: TimerUpdateData) =>
    api.post<TimerSession>(`/timer/${sessionId}/stop`, data)
}
