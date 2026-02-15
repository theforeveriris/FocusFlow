<template>
  <ErrorBoundary>
    <div class="space-y-6 animate-fade-in-up max-w-4xl">
      <!-- Header -->
      <div>
        <h1 class="text-2xl font-bold text-gray-900">设置</h1>
        <p class="text-gray-500 mt-1">自定义你的 FocusFlow 体验</p>
      </div>
      
      <!-- Theme Settings -->
      <BaseCard>
        <template #header>
          <div class="flex items-center gap-2">
            <Palette class="w-5 h-5 text-primary-500" />
            <h2 class="text-lg font-semibold text-gray-900">主题设置</h2>
          </div>
        </template>
        
        <div class="space-y-6">
          <!-- Theme Presets -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">
              选择主题
            </label>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="theme in themes"
                :key="theme.id"
                @click="selectTheme(theme.id)"
                class="relative cursor-pointer rounded-lg border-2 transition-all hover:shadow-md"
                :class="[
                  currentTheme === theme.id
                    ? 'border-primary-500 shadow-md'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <!-- Theme Preview -->
                <div class="p-4 space-y-3">
                  <div class="flex items-center justify-between">
                    <h3 class="font-semibold text-gray-900">{{ theme.name }}</h3>
                    <Check
                      v-if="currentTheme === theme.id"
                      class="w-5 h-5 text-primary-500"
                    />
                  </div>
                  
                  <!-- Color Preview -->
                  <div class="flex gap-2">
                    <div
                      v-for="color in theme.colors"
                      :key="color"
                      :style="{ backgroundColor: color }"
                      class="w-8 h-8 rounded-md shadow-sm"
                    ></div>
                  </div>
                  
                  <p class="text-xs text-gray-500">{{ theme.description }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Custom Colors -->
          <div class="pt-6 border-t border-gray-200">
            <label class="block text-sm font-medium text-gray-700 mb-3">
              自定义主色调
            </label>
            <div class="flex items-center gap-4">
              <input
                v-model="customPrimaryColor"
                type="color"
                class="w-16 h-16 rounded-lg cursor-pointer border-2 border-gray-300"
              />
              <div class="flex-1">
                <p class="text-sm text-gray-600">选择你喜欢的主色调</p>
                <p class="text-xs text-gray-500 mt-1">当前颜色: {{ customPrimaryColor }}</p>
              </div>
              <button
                @click="applyCustomColor"
                class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                应用
              </button>
            </div>
          </div>
        </div>
      </BaseCard>
      
      <!-- Display Settings -->
      <BaseCard>
        <template #header>
          <div class="flex items-center gap-2">
            <Monitor class="w-5 h-5 text-primary-500" />
            <h2 class="text-lg font-semibold text-gray-900">显示设置</h2>
          </div>
        </template>
        
        <div class="space-y-4">
          <!-- Font Size -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              字体大小
            </label>
            <div class="flex items-center gap-4">
              <input
                v-model="fontSize"
                type="range"
                min="12"
                max="18"
                step="1"
                class="flex-1"
              />
              <span class="text-sm text-gray-600 w-16">{{ fontSize }}px</span>
            </div>
          </div>
          
          <!-- Sidebar Width -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              侧边栏宽度
            </label>
            <div class="flex items-center gap-4">
              <input
                v-model="sidebarWidth"
                type="range"
                min="200"
                max="320"
                step="20"
                class="flex-1"
              />
              <span class="text-sm text-gray-600 w-16">{{ sidebarWidth }}px</span>
            </div>
          </div>
          
          <!-- Card Radius -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              卡片圆角
            </label>
            <div class="flex items-center gap-4">
              <input
                v-model="cardRadius"
                type="range"
                min="0"
                max="24"
                step="4"
                class="flex-1"
              />
              <span class="text-sm text-gray-600 w-16">{{ cardRadius }}px</span>
            </div>
          </div>
          
          <!-- Compact Mode -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-200">
            <div>
              <label class="text-sm font-medium text-gray-700">紧凑模式</label>
              <p class="text-xs text-gray-500 mt-1">减少间距，显示更多内容</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="compactMode"
                type="checkbox"
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
          
          <!-- Dark Mode -->
          <div class="flex items-center justify-between">
            <div>
              <label class="text-sm font-medium text-gray-700">深色模式</label>
              <p class="text-xs text-gray-500 mt-1">切换到深色主题</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="darkMode"
                type="checkbox"
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>
      </BaseCard>
      
      <!-- Animation Settings -->
      <BaseCard>
        <template #header>
          <div class="flex items-center gap-2">
            <Sparkles class="w-5 h-5 text-primary-500" />
            <h2 class="text-lg font-semibold text-gray-900">动画设置</h2>
          </div>
        </template>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <label class="text-sm font-medium text-gray-700">启用动画</label>
              <p class="text-xs text-gray-500 mt-1">页面切换和元素动画效果</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="enableAnimations"
                type="checkbox"
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>
      </BaseCard>
      
      <!-- Action Buttons -->
      <div class="flex items-center gap-4">
        <button
          @click="saveSettings"
          class="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
        >
          <Save class="w-4 h-4 inline-block mr-2" />
          保存设置
        </button>
        
        <button
          @click="resetSettings"
          class="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
        >
          <RotateCcw class="w-4 h-4 inline-block mr-2" />
          恢复默认
        </button>
      </div>
    </div>
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { 
  Palette, Monitor, Sparkles, Check, 
  Save, RotateCcw 
} from 'lucide-vue-next'
import BaseCard from '@/components/common/BaseCard.vue'
import ErrorBoundary from '@/components/common/ErrorBoundary.vue'

interface Theme {
  id: string
  name: string
  description: string
  colors: string[]
  primaryColor: string
}

// Themes
const themes: Theme[] = [
  {
    id: 'default',
    name: '默认蓝',
    description: '经典的蓝色主题，专业且清爽',
    colors: ['#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
    primaryColor: '#3b82f6'
  },
  {
    id: 'purple',
    name: '优雅紫',
    description: '优雅的紫色主题，富有创意',
    colors: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ede9fe'],
    primaryColor: '#8b5cf6'
  },
  {
    id: 'green',
    name: '自然绿',
    description: '清新的绿色主题，护眼舒适',
    colors: ['#10b981', '#34d399', '#6ee7b7', '#d1fae5'],
    primaryColor: '#10b981'
  },
  {
    id: 'orange',
    name: '活力橙',
    description: '充满活力的橙色主题',
    colors: ['#f59e0b', '#fbbf24', '#fcd34d', '#fef3c7'],
    primaryColor: '#f59e0b'
  },
  {
    id: 'pink',
    name: '温柔粉',
    description: '温柔的粉色主题，柔和可爱',
    colors: ['#ec4899', '#f472b6', '#f9a8d4', '#fce7f3'],
    primaryColor: '#ec4899'
  },
  {
    id: 'teal',
    name: '青色',
    description: '现代的青色主题，清新明快',
    colors: ['#14b8a6', '#2dd4bf', '#5eead4', '#ccfbf1'],
    primaryColor: '#14b8a6'
  }
]

// State
const currentTheme = ref('default')
const customPrimaryColor = ref('#3b82f6')
const fontSize = ref(14)
const sidebarWidth = ref(256)
const cardRadius = ref(8)
const compactMode = ref(false)
const darkMode = ref(false)
const enableAnimations = ref(true)

// Methods
const selectTheme = (themeId: string) => {
  currentTheme.value = themeId
  const theme = themes.find(t => t.id === themeId)
  if (theme) {
    customPrimaryColor.value = theme.primaryColor
    applyTheme(theme.primaryColor)
  }
}

const applyCustomColor = () => {
  applyTheme(customPrimaryColor.value)
  currentTheme.value = 'custom'
}

const applyTheme = (primaryColor: string) => {
  // Convert hex to RGB
  const hex = primaryColor.replace('#', '')
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  
  // Set CSS variables
  document.documentElement.style.setProperty('--color-primary-500', primaryColor)
  document.documentElement.style.setProperty('--color-primary-rgb', `${r}, ${g}, ${b}`)
  
  // Generate lighter and darker shades
  const lighter = `rgb(${Math.min(r + 40, 255)}, ${Math.min(g + 40, 255)}, ${Math.min(b + 40, 255)})`
  const darker = `rgb(${Math.max(r - 40, 0)}, ${Math.max(g - 40, 0)}, ${Math.max(b - 40, 0)})`
  
  document.documentElement.style.setProperty('--color-primary-400', lighter)
  document.documentElement.style.setProperty('--color-primary-600', darker)
}

const saveSettings = () => {
  const settings = {
    theme: currentTheme.value,
    customPrimaryColor: customPrimaryColor.value,
    fontSize: fontSize.value,
    sidebarWidth: sidebarWidth.value,
    cardRadius: cardRadius.value,
    compactMode: compactMode.value,
    darkMode: darkMode.value,
    enableAnimations: enableAnimations.value
  }
  
  localStorage.setItem('focusflow-settings', JSON.stringify(settings))
  
  // Apply settings
  applyAllSettings()
  
  alert('设置已保存！')
}

const resetSettings = () => {
  if (confirm('确定要恢复默认设置吗？')) {
    localStorage.removeItem('focusflow-settings')
    
    // Reset to defaults
    currentTheme.value = 'default'
    customPrimaryColor.value = '#3b82f6'
    fontSize.value = 14
    sidebarWidth.value = 256
    cardRadius.value = 8
    compactMode.value = false
    darkMode.value = false
    enableAnimations.value = true
    
    applyAllSettings()
    
    alert('已恢复默认设置！')
  }
}

const applyAllSettings = () => {
  // Apply theme
  applyTheme(customPrimaryColor.value)
  
  // Apply font size
  document.documentElement.style.setProperty('--font-size-base', `${fontSize.value}px`)
  
  // Apply card radius
  document.documentElement.style.setProperty('--card-radius', `${cardRadius.value}px`)
  
  // Apply compact mode
  if (compactMode.value) {
    document.documentElement.classList.add('compact-mode')
  } else {
    document.documentElement.classList.remove('compact-mode')
  }
  
  // Apply dark mode
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  
  // Apply animations
  if (!enableAnimations.value) {
    document.documentElement.classList.add('no-animations')
  } else {
    document.documentElement.classList.remove('no-animations')
  }
}

const loadSettings = () => {
  const saved = localStorage.getItem('focusflow-settings')
  if (saved) {
    try {
      const settings = JSON.parse(saved)
      currentTheme.value = settings.theme || 'default'
      customPrimaryColor.value = settings.customPrimaryColor || '#3b82f6'
      fontSize.value = settings.fontSize || 14
      sidebarWidth.value = settings.sidebarWidth || 256
      cardRadius.value = settings.cardRadius || 8
      compactMode.value = settings.compactMode || false
      darkMode.value = settings.darkMode || false
      enableAnimations.value = settings.enableAnimations !== false
      
      applyAllSettings()
    } catch (e) {
      console.error('Failed to load settings:', e)
    }
  }
}

// Watch for changes
watch([fontSize, cardRadius, compactMode, darkMode, enableAnimations], () => {
  applyAllSettings()
})

// Lifecycle
onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
input[type="range"] {
  @apply appearance-none bg-gray-200 rounded-lg h-2 outline-none;
}

input[type="range"]::-webkit-slider-thumb {
  @apply appearance-none w-4 h-4 bg-primary-500 rounded-full cursor-pointer;
}

input[type="range"]::-moz-range-thumb {
  @apply w-4 h-4 bg-primary-500 rounded-full cursor-pointer border-0;
}
</style>
