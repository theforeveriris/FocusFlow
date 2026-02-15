import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { projectApi } from '@/api/projects'
import type { Project, ProjectCreate } from '@/types'

export const useProjectStore = defineStore('projects', () => {
  // State
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const activeProjects = computed(() => projects.value.filter(p => p.status === 'active'))
  const archivedProjects = computed(() => projects.value.filter(p => p.status === 'archived'))
  
  const projectsWithStats = computed(() => {
    return projects.value.map(p => ({
      ...p,
      completionRate: p.plan_count > 0 ? Math.round((p.progress / 100) * p.plan_count) : 0
    }))
  })

  // Actions
  const fetchProjects = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await projectApi.getAll()
      projects.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects'
    } finally {
      loading.value = false
    }
  }

  const fetchProjectById = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await projectApi.getById(id)
      currentProject.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project'
      return null
    } finally {
      loading.value = false
    }
  }

  const createProject = async (data: ProjectCreate) => {
    loading.value = true
    error.value = null
    try {
      const response = await projectApi.create(data)
      projects.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create project'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateProject = async (id: number, data: Partial<ProjectCreate>) => {
    loading.value = true
    error.value = null
    try {
      const response = await projectApi.update(id, data)
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = response.data
      }
      if (currentProject.value?.id === id) {
        currentProject.value = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update project'
      return null
    } finally {
      loading.value = false
    }
  }

  const deleteProject = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await projectApi.delete(id)
      projects.value = projects.value.filter(p => p.id !== id)
      if (currentProject.value?.id === id) {
        currentProject.value = null
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete project'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    activeProjects,
    archivedProjects,
    projectsWithStats,
    fetchProjects,
    fetchProjectById,
    createProject,
    updateProject,
    deleteProject
  }
})
