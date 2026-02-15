import { createRouter, createWebHistory } from 'vue-router'
import { useAppStore } from '@/stores'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/plans'
    },
    {
      path: '/plans',
      name: 'plans',
      component: () => import('@/views/PlansView.vue'),
      meta: {
        title: '计划管理',
        icon: 'ClipboardList'
      }
    },
    {
      path: '/archive',
      name: 'archive',
      component: () => import('@/views/ArchiveView.vue'),
      meta: {
        title: '已完成计划',
        icon: 'Archive'
      }
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/ProjectsView.vue'),
      meta: {
        title: '项目管理',
        icon: 'FolderKanban'
      }
    },
    {
      path: '/timer',
      name: 'timer',
      component: () => import('@/views/TimeTrackingView.vue'),
      meta: {
        title: '时间追踪',
        icon: 'Timer'
      }
    },
    {
      path: '/timer-calendar',
      name: 'timer-calendar',
      component: () => import('@/views/TimeTrackingCalendarView.vue'),
      meta: {
        title: '时间可视化',
        icon: 'Calendar'
      }
    },
    {
      path: '/timer-debug',
      name: 'timer-debug',
      component: () => import('@/views/TimeTrackingDebug.vue'),
      meta: {
        title: '时间追踪调试',
        icon: 'Timer'
      }
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('@/views/StatisticsView.vue'),
      meta: {
        title: '数据统计',
        icon: 'BarChart3'
      }
    },
    {
      path: '/accounting',
      name: 'accounting',
      component: () => import('@/views/AccountingView.vue'),
      meta: {
        title: '记账',
        icon: 'Wallet'
      }
    },
    {
      path: '/accounting/account/:id',
      name: 'account-detail',
      component: () => import('@/views/AccountDetailView.vue'),
      meta: {
        title: '账户详情',
        icon: 'Wallet'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: {
        title: '设置',
        icon: 'Settings'
      }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  appStore.setLoading(true)
  
  // Set page title
  if (to.meta.title) {
    document.title = `${to.meta.title} - FocusFlow`
  }
  
  next()
})

router.afterEach(() => {
  const appStore = useAppStore()
  setTimeout(() => {
    appStore.setLoading(false)
  }, 300)
})

// 捕获路由错误
router.onError((error) => {
  console.error('路由错误:', error)
  
  // 如果是加载组件失败，尝试刷新
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    console.log('检测到模块加载失败，准备刷新页面...')
    alert('页面资源加载失败，即将刷新页面')
    window.location.reload()
  }
})

export default router
