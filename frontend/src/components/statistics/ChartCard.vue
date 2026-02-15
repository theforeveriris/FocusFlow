<template>
  <BaseCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900">{{ title }}</h3>
        
        <!-- Time Range Selector -->
        <select
          :value="timeRange"
          @change="$emit('update:timeRange', ($event.target as HTMLSelectElement).value)"
          class="px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500"
        >
          <option value="today">今天</option>
          <option value="week">本周</option>
          <option value="month">本月</option>
          <option value="year">今年</option>
        </select>
      </div>
    </template>
    
    <slot></slot>
  </BaseCard>
</template>

<script setup lang="ts">
import BaseCard from '@/components/common/BaseCard.vue'

defineProps<{
  title: string
  timeRange: string
}>()

defineEmits<{
  'update:timeRange': [value: string]
}>()
</script>
