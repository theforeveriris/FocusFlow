<template>
  <Teleport to="body">
    <Transition name="zen">
      <div v-if="modelValue" class="fixed inset-0 z-[100] bg-gray-900 flex flex-col items-center justify-center">
        <!-- Close Button -->
        <button
          @click="$emit('update:modelValue', false)"
          class="absolute top-6 right-6 p-3 rounded-full bg-gray-800 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
        >
          <Minimize2 class="w-6 h-6" />
        </button>
        
        <!-- Timer Display -->
        <div class="text-center">
          <div class="text-[12rem] font-mono font-bold text-white tracking-wider leading-none">
            {{ time }}
          </div>
          
          <!-- Quote -->
          <p class="mt-8 text-xl text-gray-400 italic max-w-lg mx-auto">
            "{{ quote }}"
          </p>
        </div>
        
        <!-- Stop Button -->
        <button
          @click="$emit('stop')"
          class="mt-16 px-8 py-4 bg-red-500 hover:bg-red-600 text-white rounded-full text-lg font-medium transition-colors flex items-center gap-2"
        >
          <Square class="w-5 h-5" />
          结束专注
        </button>
        
        <!-- Tip -->
        <p class="absolute bottom-8 text-gray-500 text-sm">
          按 ESC 退出 Zen 模式
        </p>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { Minimize2, Square } from 'lucide-vue-next'

interface Props {
  modelValue: boolean
  time: string
  quote: string
}

defineProps<Props>()

defineEmits<{
  'update:modelValue': [value: boolean]
  stop: []
}>()
</script>

<style scoped>
.zen-enter-active,
.zen-leave-active {
  transition: opacity 0.5s ease;
}

.zen-enter-from,
.zen-leave-to {
  opacity: 0;
}
</style>
