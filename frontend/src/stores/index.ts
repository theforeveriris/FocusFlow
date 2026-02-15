import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Global app store
export const useAppStore = defineStore('app', () => {
  // State
  const sidebarCollapsed = ref(false)
  const currentTheme = ref('light')
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isDark = computed(() => currentTheme.value === 'dark')

  // Actions
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setTheme = (theme: string) => {
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
  }

  const initTheme = () => {
    const saved = localStorage.getItem('theme')
    if (saved) {
      currentTheme.value = saved
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      currentTheme.value = 'dark'
    }
  }

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  return {
    sidebarCollapsed,
    currentTheme,
    isLoading,
    error,
    isDark,
    toggleSidebar,
    setTheme,
    initTheme,
    setLoading,
    setError
  }
})
