<template>
  <ErrorBoundary>
    <div class="min-h-screen bg-gray-50">
      <!-- Top Navigation -->
      <TopNav />
      
      <div class="flex">
        <!-- Sidebar -->
        <Sidebar />
        
        <!-- Main Content -->
        <main 
          class="flex-1 transition-all duration-300"
          :class="{ 'ml-16': sidebarCollapsed, 'ml-64': !sidebarCollapsed }"
        >
          <div class="pt-16 px-6 py-6">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <ErrorBoundary>
                  <component :is="Component" />
                </ErrorBoundary>
              </transition>
            </router-view>
          </div>
        </main>
      </div>
      
      <!-- Loading Overlay -->
      <LoadingOverlay v-if="isLoading" />
    </div>
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAppStore } from '@/stores'
import TopNav from '@/components/layout/TopNav.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import LoadingOverlay from '@/components/common/LoadingOverlay.vue'
import ErrorBoundary from '@/components/common/ErrorBoundary.vue'

const appStore = useAppStore()
const sidebarCollapsed = computed(() => appStore.sidebarCollapsed)
const isLoading = computed(() => appStore.isLoading)

onMounted(() => {
  appStore.initTheme()
  
  // 加载保存的设置（包括深色模式）
  const saved = localStorage.getItem('focusflow-settings')
  if (saved) {
    try {
      const settings = JSON.parse(saved)
      if (settings.darkMode) {
        document.documentElement.classList.add('dark')
        appStore.setTheme('dark')
      }
    } catch (e) {
      console.error('Failed to load settings:', e)
    }
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
