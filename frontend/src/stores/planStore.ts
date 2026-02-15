import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { planApi } from '@/api/plans'
import type { Plan, PlanCreate } from '@/types'

export const usePlanStore = defineStore('plans', () => {
  // State
  const plans = ref<Plan[]>([])
  const currentPlan = ref<Plan | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const todoPlans = computed(() => plans.value.filter(p => p.status === 'todo'))
  const inProgressPlans = computed(() => plans.value.filter(p => p.status === 'in_progress'))
  const completedPlans = computed(() => plans.value.filter(p => p.status === 'completed'))
  
  const plansByPriority = computed(() => ({
    urgent_important: plans.value.filter(p => p.priority_matrix === 'urgent_important'),
    not_urgent_important: plans.value.filter(p => p.priority_matrix === 'not_urgent_important'),
    urgent_not_important: plans.value.filter(p => p.priority_matrix === 'urgent_not_important'),
    not_urgent_not_important: plans.value.filter(p => p.priority_matrix === 'not_urgent_not_important')
  }))

  // Actions
  const fetchPlans = async (params?: { 
    project_id?: number
    status?: string
    start_date?: string
    end_date?: string
    exclude_completed?: boolean
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await planApi.getAll(params)
      plans.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch plans'
    } finally {
      loading.value = false
    }
  }

  const fetchPlanById = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await planApi.getById(id)
      currentPlan.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch plan'
      return null
    } finally {
      loading.value = false
    }
  }

  const createPlan = async (data: PlanCreate) => {
    loading.value = true
    error.value = null
    try {
      const response = await planApi.create(data)
      plans.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create plan'
      return null
    } finally {
      loading.value = false
    }
  }

  const updatePlan = async (id: number, data: Partial<PlanCreate>) => {
    loading.value = true
    error.value = null
    try {
      const response = await planApi.update(id, data)
      const index = plans.value.findIndex(p => p.id === id)
      if (index !== -1) {
        plans.value[index] = response.data
      }
      if (currentPlan.value?.id === id) {
        currentPlan.value = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update plan'
      return null
    } finally {
      loading.value = false
    }
  }

  const deletePlan = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await planApi.delete(id)
      plans.value = plans.value.filter(p => p.id !== id)
      if (currentPlan.value?.id === id) {
        currentPlan.value = null
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete plan'
      return false
    } finally {
      loading.value = false
    }
  }

  const updatePlanStatus = async (id: number, status: string) => {
    try {
      await planApi.updateStatus(id, status)
      const plan = plans.value.find(p => p.id === id)
      if (plan) {
        plan.status = status as any
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update status'
      return false
    }
  }

  return {
    plans,
    currentPlan,
    loading,
    error,
    todoPlans,
    inProgressPlans,
    completedPlans,
    plansByPriority,
    fetchPlans,
    fetchPlanById,
    createPlan,
    updatePlan,
    deletePlan,
    updatePlanStatus
  }
})
