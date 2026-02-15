<template>
  <div class="bg-white rounded-xl border border-gray-200 overflow-hidden card-hover group">
    <!-- Header with color -->
    <div 
      class="h-20 flex items-end p-4"
      :style="{ backgroundColor: project.color + '20' }"
    >
      <div 
        class="w-12 h-12 rounded-xl flex items-center justify-center shadow-sm"
        :style="{ backgroundColor: project.color }"
      >
        <FolderKanban class="w-6 h-6 text-white" />
      </div>
    </div>
    
    <!-- Content -->
    <div class="p-4">
      <div class="flex items-start justify-between">
        <div>
          <h3 class="font-semibold text-gray-900">{{ project.name }}</h3>
          <p v-if="project.description" class="text-sm text-gray-500 mt-1 line-clamp-2">
            {{ project.description }}
          </p>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            @click="$emit('edit', project)"
            class="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
          >
            <Pencil class="w-4 h-4" />
          </button>
          <button
            @click="$emit('delete', project.id)"
            class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>
      </div>
      
      <!-- Progress -->
      <div class="mt-4">
        <div class="flex items-center justify-between text-sm mb-1">
          <span class="text-gray-500">进度</span>
          <span class="font-medium text-gray-900">{{ project.progress }}%</span>
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{ width: project.progress + '%', backgroundColor: project.color }"
          />
        </div>
      </div>
      
      <!-- Stats -->
      <div class="flex items-center gap-4 mt-4 text-sm text-gray-500">
        <span class="flex items-center gap-1">
          <ClipboardList class="w-4 h-4" />
          {{ project.plan_count }} 计划
        </span>
        <span v-if="project.start_date" class="flex items-center gap-1">
          <Calendar class="w-4 h-4" />
          {{ formatDate(project.start_date) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FolderKanban, Pencil, Trash2, ClipboardList, Calendar } from 'lucide-vue-next'
import { formatDate } from '@/utils/helpers'
import type { Project } from '@/types'

interface Props {
  project: Project
}

defineProps<Props>()

defineEmits<{
  edit: [project: Project]
  delete: [id: number]
}>()
</script>
