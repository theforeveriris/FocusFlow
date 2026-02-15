<template>
  <div
    class="bg-white rounded-lg border border-gray-200 transition-all duration-200"
    :class="{ 'card-hover': hoverable, 'shadow-sm': !flat, 'p-4': padding }"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  hoverable?: boolean
  flat?: boolean
  padding?: boolean
}

withDefaults(defineProps<Props>(), {
  hoverable: false,
  flat: false,
  padding: true
})
</script>
