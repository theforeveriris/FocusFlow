<template>
  <aside 
    class="fixed left-0 top-16 bottom-0 bg-white border-r border-gray-200 transition-all duration-300 z-40"
    :class="{ 'w-16': sidebarCollapsed, 'w-64': !sidebarCollapsed }"
  >
    <nav class="p-2 space-y-1">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200"
        :class="[
          isActive(item.path) 
            ? 'bg-primary-50 text-primary-600' 
            : 'text-gray-600 hover:bg-gray-100'
        ]"
      >
        <component :is="getIcon(item.icon)" class="w-5 h-5 flex-shrink-0" />
        <span 
          class="text-sm font-medium whitespace-nowrap transition-opacity duration-300"
          :class="{ 'opacity-0 w-0': sidebarCollapsed, 'opacity-100': !sidebarCollapsed }"
        >
          {{ item.name }}
        </span>
      </router-link>
    </nav>
    
    <!-- Bottom Actions -->
    <div class="absolute bottom-0 left-0 right-0 p-2 border-t border-gray-200">
      <router-link
        to="/settings"
        class="flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 w-full"
        :class="[
          isActive('/settings') 
            ? 'bg-primary-50 text-primary-600' 
            : 'text-gray-600 hover:bg-gray-100'
        ]"
      >
        <Settings class="w-5 h-5 flex-shrink-0" />
        <span 
          class="text-sm font-medium whitespace-nowrap transition-opacity duration-300"
          :class="{ 'opacity-0 w-0': sidebarCollapsed, 'opacity-100': !sidebarCollapsed }"
        >
          设置
        </span>
      </router-link>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import {
  ClipboardList,
  FolderKanban,
  Timer,
  Calendar,
  BarChart3,
  Wallet,
  Archive,
  Settings
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

const sidebarCollapsed = computed(() => appStore.sidebarCollapsed)

const navItems = [
  { name: '计划管理', path: '/plans', icon: 'ClipboardList' },
  { name: '已完成', path: '/archive', icon: 'Archive' },
  { name: '项目管理', path: '/projects', icon: 'FolderKanban' },
  { name: '时间追踪', path: '/timer', icon: 'Timer' },
  { name: '时间可视化', path: '/timer-calendar', icon: 'Calendar' },
  { name: '记账', path: '/accounting', icon: 'Wallet' },
  { name: '数据统计', path: '/statistics', icon: 'BarChart3' }
]

const iconMap: Record<string, any> = {
  ClipboardList,
  Archive,
  FolderKanban,
  Timer,
  Calendar,
  BarChart3,
  Wallet
}

const getIcon = (name: string) => iconMap[name] || ClipboardList

const isActive = (path: string) => route.path === path || route.path.startsWith(path + '/')
</script>
