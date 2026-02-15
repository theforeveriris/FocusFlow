import api from './index'
import type { Plan, PlanCreate } from '@/types'

export const planApi = {
  // Get all plans
  getAll: (params?: { project_id?: number; status?: string; priority?: string }) =>
    api.get<Plan[]>('/plans', { params }),

  // Get plan tree
  getTree: (project_id?: number) =>
    api.get<Plan[]>('/plans/tree', { params: { project_id } }),

  // Get plan by ID
  getById: (id: number) =>
    api.get<Plan>(`/plans/${id}`),

  // Create plan
  create: (data: PlanCreate) =>
    api.post<Plan>('/plans', data),

  // Update plan
  update: (id: number, data: Partial<PlanCreate>) =>
    api.put<Plan>(`/plans/${id}`, data),

  // Delete plan
  delete: (id: number) =>
    api.delete(`/plans/${id}`),

  // Update plan status
  updateStatus: (id: number, status: string) =>
    api.patch(`/plans/${id}/status`, null, { params: { status } })
}
