<template>
  <header class="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-50">
    <div class="flex items-center justify-between h-full px-4">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <button
          @click="toggleSidebar"
          class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Menu class="w-5 h-5 text-gray-600" />
        </button>
        <router-link to="/" class="flex items-center gap-2">
          <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
            <Zap class="w-5 h-5 text-white" />
          </div>
          <span class="text-xl font-bold text-gray-900">FocusFlow</span>
        </router-link>
      </div>
      
      <!-- Right Actions -->
      <div class="flex items-center gap-2">
        <!-- Quick Timer -->
        <button
          @click="goToTimer"
          class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Timer class="w-5 h-5 text-gray-600" />
          <span class="text-sm text-gray-700 hidden sm:block">专注</span>
        </button>
        
        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Sun v-if="isDark" class="w-5 h-5 text-gray-600" />
          <Moon v-else class="w-5 h-5 text-gray-600" />
        </button>
        
        <!-- User Menu / Settings -->
        <button
          @click="goToSettings"
          class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          title="设置"
        >
          <User class="w-5 h-5 text-gray-600" />
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { Menu, Zap, Timer, Sun, Moon, User } from 'lucide-vue-next'

const router = useRouter()
const appStore = useAppStore()

const isDark = computed(() => appStore.isDark)

const toggleSidebar = () => {
  appStore.toggleSidebar()
}

const toggleTheme = () => {
  const newTheme = isDark.value ? 'light' : 'dark'
  appStore.setTheme(newTheme)
  
  // 同步到 HTML 元素
  if (newTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  
  // 同步到 localStorage
  const settings = JSON.parse(localStorage.getItem('focusflow-settings') || '{}')
  settings.darkMode = newTheme === 'dark'
  localStorage.setItem('focusflow-settings', JSON.stringify(settings))
}

const goToTimer = () => {
  router.push('/timer')
}

const goToSettings = () => {
  router.push('/settings')
}
</script>
