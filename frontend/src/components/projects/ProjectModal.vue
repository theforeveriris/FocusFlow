<template>
  <BaseModal
    v-model="visible"
    :title="project ? '编辑项目' : '新建项目'"
    @update:modelValue="$emit('update:modelValue', $event)"
  >
    <form @submit.prevent="save" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">名称</label>
        <input
          v-model="form.name"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          placeholder="输入项目名称"
        />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
        <textarea
          v-model="form.description"
          rows="3"
          class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          placeholder="输入项目描述"
        />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">主题色</label>
        <div class="flex items-center gap-3">
          <input
            v-model="form.color"
            type="color"
            class="w-10 h-10 rounded-lg border border-gray-200 cursor-pointer"
          />
          <span class="text-sm text-gray-500">{{ form.color }}</span>
        </div>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">开始日期</label>
          <input
            v-model="form.start_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">结束日期</label>
          <input
            v-model="form.end_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
        </div>
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
import { ref, computed, watch } from 'vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import type { Project, ProjectCreate } from '@/types'

interface Props {
  modelValue: boolean
  project?: Project | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: ProjectCreate]
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const loading = ref(false)

const form = ref<ProjectCreate>({
  name: '',
  description: '',
  color: '#3b82f6',
  start_date: undefined,
  end_date: undefined
})

watch(() => props.project, (newProject) => {
  if (newProject) {
    form.value = {
      name: newProject.name,
      description: newProject.description || '',
      color: newProject.color,
      start_date: newProject.start_date,
      end_date: newProject.end_date
    }
  } else {
    form.value = {
      name: '',
      description: '',
      color: '#3b82f6',
      start_date: undefined,
      end_date: undefined
    }
  }
}, { immediate: true })

const save = () => {
  if (!form.value.name) return
  emit('save', form.value)
}
</script>
