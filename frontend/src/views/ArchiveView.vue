<template>
  <div class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">已完成计划</h1>
        <p class="text-gray-500 mt-1">查看已归档的完成计划</p>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="flex items-center justify-between bg-white p-3 rounded-lg border border-gray-200">
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
          v-model="filterPriority"
          class="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        >
          <option value="">全部优先级</option>
          <option value="urgent_important">紧急且重要</option>
          <option value="not_urgent_important">重要不紧急</option>
          <option value="urgent_not_important">紧急不重要</option>
          <option value="not_urgent_not_important">不紧急不重要</option>
        </select>
      </div>
      
      <div class="text-sm text-gray-500">
        共 {{ filteredPlans.length }} 个已完成计划
      </div>
    </div>
    
    <!-- Content -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 text-primary-500 animate-spin" />
    </div>
    
    <div v-else class="space-y-3">
      <PlanCard
        v-for="plan in filteredPlans"
        :key="plan.id"
        :plan="plan"
        @edit="editPlan"
        @delete="deletePlan"
      />
      
      <div v-if="filteredPlans.length === 0" class="text-center py-12 text-gray-500">
        <Archive class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p>暂无已完成的计划</p>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <PlanModal
      v-model="showEditModal"
      :plan="editingPlan"
      @save="savePlan"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { usePlanStore } from '@/stores/planStore'
import { Archive, Loader2 } from 'lucide-vue-next'
import PlanCard from '@/components/plans/PlanCard.vue'
import PlanModal from '@/components/plans/PlanModal.vue'
import type { Plan, PlanCreate } from '@/types'

const planStore = usePlanStore()

// State
const filterPriority = ref('')
const filterStartDate = ref('')
const filterEndDate = ref('')
const showEditModal = ref(false)
const editingPlan = ref<Plan | null>(null)

// Computed
const loading = computed(() => planStore.loading)
const plans = computed(() => planStore.plans)

const filteredPlans = computed(() => {
  let result = plans.value
  
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
  const params: any = {
    status: 'completed',
    exclude_completed: false
  }
  
  if (filterStartDate.value) {
    params.start_date = new Date(filterStartDate.value).toISOString()
  }
  
  if (filterEndDate.value) {
    params.end_date = new Date(filterEndDate.value).toISOString()
  }
  
  planStore.fetchPlans(params)
}

// Watch filters and reload
watch([filterStartDate, filterEndDate], () => {
  loadPlans()
})

const editPlan = (plan: Plan) => {
  editingPlan.value = plan
  showEditModal.value = true
}

const deletePlan = async (id: number) => {
  if (confirm('确定要删除这个计划吗？')) {
    await planStore.deletePlan(id)
    loadPlans()
  }
}

const savePlan = async (data: PlanCreate) => {
  if (editingPlan.value) {
    await planStore.updatePlan(editingPlan.value.id, data)
    loadPlans()
  }
  showEditModal.value = false
  editingPlan.value = null
}
</script>
