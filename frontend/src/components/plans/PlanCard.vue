<template>
  <div
    class="bg-white rounded-lg border border-gray-200 transition-all duration-200 card-hover relative"
    :class="{ 'p-3': compact, 'p-4': !compact }"
    :style="{ borderLeftWidth: '4px', borderLeftColor: getPriorityColor(plan.priority_matrix) }"
  >
    <div class="flex items-start gap-3">
      <!-- Checkbox -->
      <input
        type="checkbox"
        :checked="plan.status === 'completed'"
        @change="toggleStatus"
        class="mt-1 w-5 h-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
      />
      
      <!-- Content -->
      <div class="flex-1 min-w-0">
        <div class="flex items-start justify-between gap-2">
          <h4 
            class="font-medium text-gray-900 truncate"
            :class="{ 'line-through text-gray-400': plan.status === 'completed' }"
          >
            {{ plan.title }}
          </h4>
          
          <!-- Actions -->
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              @click="$emit('edit', plan)"
              class="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
            >
              <Pencil class="w-4 h-4" />
            </button>
            <button
              @click="$emit('delete', plan.id)"
              class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <p v-if="plan.description && !compact" class="text-sm text-gray-500 mt-1 line-clamp-2">
          {{ plan.description }}
        </p>
        
        <!-- Meta -->
        <div class="flex items-center gap-3 mt-2 text-xs text-gray-400">
          <span 
            class="px-2 py-0.5 rounded-full"
            :style="{ backgroundColor: getPriorityColor(plan.priority_matrix) + '20', color: getPriorityColor(plan.priority_matrix) }"
          >
            {{ getPriorityLabel(plan.priority_matrix) }}
          </span>
          
          <span v-if="plan.project_name" class="flex items-center gap-1">
            <FolderKanban class="w-3 h-3" />
            {{ plan.project_name }}
          </span>
          
          <span v-if="plan.start_time" class="flex items-center gap-1">
            <Clock class="w-3 h-3" />
            {{ formatDate(plan.start_time) }}
          </span>
          
          <span v-if="plan.actual_duration > 0" class="flex items-center gap-1">
            <Timer class="w-3 h-3" />
            {{ formatDuration(plan.actual_duration * 60) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Pencil, Trash2, FolderKanban, Clock, Timer } from 'lucide-vue-next'
import { getPriorityLabel, getPriorityColor, formatDate, formatDuration } from '@/utils/helpers'
import type { Plan } from '@/types'

interface Props {
  plan: Plan
  compact?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  edit: [plan: Plan]
  delete: [id: number]
  statusChange: [id: number, status: string]
}>()

const toggleStatus = () => {
  const newStatus = props.plan.status === 'completed' ? 'todo' : 'completed'
  emit('statusChange', props.plan.id, newStatus)
}
</script>
