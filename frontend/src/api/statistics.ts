import api from './index'
import type { ProjectStats, HeatmapData, EfficiencyData, MonthlyFinance } from '@/types'

export const statisticsApi = {
  // Get overview
  getOverview: () =>
    api.get<{
      timer: {
        today_duration: number
        today_sessions: number
        today_focus_score?: number
      }
      finance: {
        total_income: number
        total_expense: number
        balance: number
      }
    }>('/statistics/overview'),

  // Get project statistics
  getProjectStats: (params?: { start_date?: string; end_date?: string }) =>
    api.get<ProjectStats[]>('/statistics/projects', { params }),

  // Get heatmap data
  getHeatmap: (days?: number) =>
    api.get<HeatmapData[]>('/statistics/heatmap', { params: { days } }),

  // Get efficiency curve
  getEfficiency: (days?: number) =>
    api.get<EfficiencyData[]>('/statistics/efficiency', { params: { days } }),

  // Get finance statistics
  getFinanceStats: (year?: number) =>
    api.get<MonthlyFinance[]>('/statistics/finance', { params: { year } })
}
