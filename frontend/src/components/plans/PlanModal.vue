<template>
  <BaseModal
    v-model="visible"
    :title="plan ? '编辑计划' : '新建计划'"
    @update:modelValue="$emit('update:modelValue', $event)"
  >
    <form @submit.prevent="save" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
        <input
          v-model="form.title"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          placeholder="输入计划标题"
        />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
        <textarea
          v-model="form.description"
          rows="3"
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          placeholder="输入计划描述"
        />
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">优先级</label>
          <select
            v-model="form.priority_matrix"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          >
            <option value="urgent_important">紧急且重要</option>
            <option value="not_urgent_important">重要不紧急</option>
            <option value="urgent_not_important">紧急不重要</option>
            <option value="not_urgent_not_important">不紧急不重要</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
          <select
            v-model="form.status"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          >
            <option value="todo">待办</option>
            <option value="in_progress">进行中</option>
            <option value="completed">已完成</option>
          </select>
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">所属项目</label>
        <select
          v-model="form.project_id"
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
        >
          <option value="">无</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.name }}
          </option>
        </select>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">开始时间</label>
          <input
            v-model="form.start_time"
            type="datetime-local"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">结束时间</label>
          <input
            v-model="form.end_time"
            type="datetime-local"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">预计时长（分钟）</label>
        <input
          v-model="form.estimated_duration"
          type="number"
          min="0"
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          placeholder="输入预计时长"
        />
      </div>
    </form>
    
    <template #footer>
      <BaseButton variant="ghost" @click="visible = false">
        取消
      </BaseButton>
      <BaseButton @click="save" :loading="loading">
        保存
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useProjectStore } from '@/stores/projectStore'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import type { Plan, PlanCreate } from '@/types'

interface Props {
  modelValue: boolean
  plan?: Plan | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: PlanCreate]
}>()

const projectStore = useProjectStore()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const loading = ref(false)
const projects = computed(() => projectStore.projects)

const form = ref<PlanCreate>({
  title: '',
  description: '',
  priority_matrix: 'not_urgent_important',
  status: 'todo',
  project_id: undefined,
  start_time: undefined,
  end_time: undefined,
  estimated_duration: undefined,
  tags: []
})

watch(() => props.plan, (newPlan) => {
  if (newPlan) {
    form.value = {
      title: newPlan.title,
      description: newPlan.description || '',
      priority_matrix: newPlan.priority_matrix,
      status: newPlan.status,
      project_id: newPlan.project_id,
      start_time: newPlan.start_time,
      end_time: newPlan.end_time,
      estimated_duration: newPlan.estimated_duration,
      tags: newPlan.tags
    }
  } else {
    form.value = {
      title: '',
      description: '',
      priority_matrix: 'not_urgent_important',
      status: 'todo',
      project_id: undefined,
      start_time: undefined,
      end_time: undefined,
      estimated_duration: undefined,
      tags: []
    }
  }
}, { immediate: true })

onMounted(() => {
  projectStore.fetchProjects()
})

const save = () => {
  if (!form.value.title) return
  
  const data: PlanCreate = {
    ...form.value,
    project_id: form.value.project_id || undefined
  }
  
  emit('save', data)
}
</script>
