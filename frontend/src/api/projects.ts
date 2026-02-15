import api from './index'
import type { Project, ProjectCreate } from '@/types'

export const projectApi = {
  // Get all projects
  getAll: () =>
    api.get<Project[]>('/projects'),

  // Get project by ID
  getById: (id: number) =>
    api.get<Project>(`/projects/${id}`),

  // Create project
  create: (data: ProjectCreate) =>
    api.post<Project>('/projects', data),

  // Update project
  update: (id: number, data: Partial<ProjectCreate>) =>
    api.put<Project>(`/projects/${id}`, data),

  // Delete project
  delete: (id: number) =>
    api.delete(`/projects/${id}`)
}
