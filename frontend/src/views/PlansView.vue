<template>
  <div class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">计划管理</h1>
        <p class="text-gray-500 mt-1">管理你的任务和计划</p>
      </div>
      <BaseButton @click="showCreateModal = true">
        <Plus class="w-4 h-4" />
        新建计划
      </BaseButton>
    </div>
    
    <!-- View Toggle & Filters -->
    <div class="flex items-center justify-between bg-white p-3 rounded-lg border border-gray-200">
      <div class="flex items-center gap-2">
        <button
          v-for="view in viewOptions"
          :key="view.value"
          @click="currentView = view.value"
          class="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors"
          :class="currentView === view.value ? 'bg-primary-50 text-primary-600' : 'text-gray-600 hover:bg-gray-100'"
        >
          <component :is="view.icon" class="w-4 h-4" />
          {{ view.label }}
        </button>
      </div>
      
      <div class="flex items-center gap-2">
        <input
          v-model="filterStartDate"
          type="date"
          placeholder="开始日期"
          class="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        />
        
        <input
          v-model="filterEndDate"
          type="date"
          placeholder="结束日期"
          class="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        />
        
        <select
          v-model="filterStatus"
          class="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        >
          <option value="">全部状态</option>
          <option value="todo">待办</option>
          <option value="in_progress">进行中</option>
        </select>
        
        <select
          v-model="filterPriority"
          class="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        >
          <option value="">全部优先级</option>
          <option value="urgent_important">紧急且重要</option>
          <option value="not_urgent_important">重要不紧急</option>
          <option value="urgent_not_important">紧急不重要</option>
          <option value="not_urgent_not_important">不紧急不重要</option>
        </select>
        
        <label class="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 cursor-pointer hover:bg-gray-50 rounded-md">
          <input
            v-model="showCompleted"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          显示已完成
        </label>
      </div>
    </div>
    
    <!-- Content -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 text-primary-500 animate-spin" />
    </div>
    
    <template v-else>
      <!-- List View -->
      <div v-if="currentView === 'list'" class="space-y-3">
        <PlanCard
          v-for="plan in filteredPlans"
          :key="plan.id"
          :plan="plan"
          @edit="editPlan"
          @delete="deletePlan"
          @status-change="updateStatus"
        />
        
        <div v-if="filteredPlans.length === 0" class="text-center py-12 text-gray-500">
          <ClipboardList class="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>暂无计划</p>
        </div>
      </div>
      
      <!-- Kanban View -->
      <div v-else-if="currentView === 'kanban'" class="grid grid-cols-2 gap-4">
        <div
          v-for="(plans, priority) in plansByPriority"
          :key="priority"
          class="bg-gray-100 rounded-lg p-4"
        >
          <div class="flex items-center gap-2 mb-4">
            <div
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: getPriorityColor(priority) }"
            />
            <h3 class="font-medium text-gray-700">{{ getPriorityLabel(priority) }}</h3>
            <span class="text-sm text-gray-500">({{ plans.length }})</span>
          </div>
          
          <div class="space-y-3">
            <PlanCard
              v-for="plan in plans"
              :key="plan.id"
              :plan="plan"
              compact
              @edit="editPlan"
              @delete="deletePlan"
              @status-change="updateStatus"
            />
          </div>
        </div>
      </div>
    </template>
    
    <!-- Create/Edit Modal -->
    <PlanModal
      v-model="showCreateModal"
      :plan="editingPlan"
      @save="savePlan"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { usePlanStore } from '@/stores/planStore'
import { Plus, List, LayoutGrid, ClipboardList, Loader2 } from 'lucide-vue-next'
import BaseButton from '@/components/common/BaseButton.vue'
import PlanCard from '@/components/plans/PlanCard.vue'
import PlanModal from '@/components/plans/PlanModal.vue'
import { getPriorityLabel, getPriorityColor } from '@/utils/helpers'
import type { Plan, PlanCreate } from '@/types'

const planStore = usePlanStore()

// State
const currentView = ref<'list' | 'kanban'>('list')
const filterStatus = ref('')
const filterPriority = ref('')
const filterStartDate = ref('')
const filterEndDate = ref('')
const showCompleted = ref(false)
const showCreateModal = ref(false)
const editingPlan = ref<Plan | null>(null)

const viewOptions = [
  { value: 'list', label: '列表', icon: List },
  { value: 'kanban', label: '看板', icon: LayoutGrid }
]

// Computed
const loading = computed(() => planStore.loading)
const plans = computed(() => planStore.plans)
const plansByPriority = computed(() => planStore.plansByPriority)

const filteredPlans = computed(() => {
  let result = plans.value
  
  if (filterStatus.value) {
    result = result.filter(p => p.status === filterStatus.value)
  }
  
  if (filterPriority.value) {
    result = result.filter(p => p.priority_matrix === filterPriority.value)
  }
  
  return result
})

// Methods
onMounted(() => {
  loadPlans()
})

const loadPlans = () => {
  const params: any = {}
  
  if (filterStartDate.value) {
    params.start_date = new Date(filterStartDate.value).toISOString()
  }
  
  if (filterEndDate.value) {
    params.end_date = new Date(filterEndDate.value).toISOString()
  }
  
  if (!showCompleted.value) {
    params.exclude_completed = true
  } else {
    params.exclude_completed = false
  }
  
  planStore.fetchPlans(params)
}

// Watch filters and reload
watch([filterStartDate, filterEndDate, showCompleted], () => {
  loadPlans()
})

const editPlan = (plan: Plan) => {
  editingPlan.value = plan
  showCreateModal.value = true
}

const deletePlan = async (id: number) => {
  if (confirm('确定要删除这个计划吗？')) {
    await planStore.deletePlan(id)
  }
}

const updateStatus = async (id: number, status: string) => {
  await planStore.updatePlanStatus(id, status)
}

const savePlan = async (data: PlanCreate) => {
  if (editingPlan.value) {
    await planStore.updatePlan(editingPlan.value.id, data)
  } else {
    await planStore.createPlan(data)
  }
  showCreateModal.value = false
  editingPlan.value = null
}
</script>
