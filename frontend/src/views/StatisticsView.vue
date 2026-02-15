<template>
  <ErrorBoundary>
    <div class="space-y-6 animate-fade-in-up">
      <!-- Header with Time Filter -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">数据统计</h1>
          <p class="text-gray-500 mt-1">查看你的生产力数据</p>
        </div>
        
        <!-- Global Time Filter -->
        <div class="flex items-center gap-2">
          <select
            v-model="globalTimeRange"
            class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            @change="onGlobalTimeRangeChange"
          >
            <option value="today">今天</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
            <option value="year">今年</option>
            <option value="custom">自定义</option>
          </select>
          
          <div v-if="globalTimeRange === 'custom'" class="flex items-center gap-2">
            <input
              v-model="customStartDate"
              type="date"
              class="px-3 py-2 border border-gray-300 rounded-lg"
              @change="onCustomDateChange"
            />
            <span class="text-gray-500">至</span>
            <input
              v-model="customEndDate"
              type="date"
              class="px-3 py-2 border border-gray-300 rounded-lg"
              @change="onCustomDateChange"
            />
          </div>
        </div>
      </div>
      
      <!-- Overview Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <BaseCard class="text-center hover:shadow-lg transition-shadow">
          <Clock class="w-8 h-8 text-primary-500 mx-auto mb-2" />
          <div class="text-3xl font-bold text-gray-900">
            {{ formatDuration(overview.total_duration) }}
          </div>
          <div class="text-sm text-gray-500">总专注时长</div>
          <div class="text-xs text-gray-400 mt-1">
            {{ overview.session_count }} 次专注
          </div>
        </BaseCard>
        
        <BaseCard class="text-center hover:shadow-lg transition-shadow">
          <Target class="w-8 h-8 text-green-500 mx-auto mb-2" />
          <div class="text-3xl font-bold text-gray-900">
            {{ overview.completed_plans }}
          </div>
          <div class="text-sm text-gray-500">完成计划</div>
          <div class="text-xs text-gray-400 mt-1">
            {{ overview.total_plans }} 个计划
          </div>
        </BaseCard>
        
        <BaseCard class="text-center hover:shadow-lg transition-shadow">
          <TrendingUp class="w-8 h-8 text-orange-500 mx-auto mb-2" />
          <div class="text-3xl font-bold text-gray-900">
            {{ safeToFixed(overview.avg_focus_score) }}
          </div>
          <div class="text-sm text-gray-500">平均专注度</div>
          <div class="text-xs text-gray-400 mt-1">
            满分 100
          </div>
        </BaseCard>
        
        <BaseCard class="text-center hover:shadow-lg transition-shadow">
          <Wallet class="w-8 h-8 text-blue-500 mx-auto mb-2" />
          <div class="text-3xl font-bold text-gray-900">
            {{ formatCurrency(overview.net_worth) }}
          </div>
          <div class="text-sm text-gray-500">净资产</div>
          <div class="text-xs text-gray-400 mt-1">
            收入 {{ formatCurrency(overview.total_income) }}
          </div>
        </BaseCard>
      </div>
      
      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 1. 时间趋势图 -->
        <ChartCard
          title="时间趋势"
          :timeRange="charts.timeTrend.timeRange"
          @update:timeRange="updateChartTimeRange('timeTrend', $event)"
        >
          <v-chart :option="timeTrendOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 2. 计划完成率 -->
        <ChartCard
          title="计划完成率"
          :timeRange="charts.planCompletion.timeRange"
          @update:timeRange="updateChartTimeRange('planCompletion', $event)"
        >
          <v-chart :option="planCompletionOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 3. 项目时间分布 -->
        <ChartCard
          title="项目时间分布"
          :timeRange="charts.projectTime.timeRange"
          @update:timeRange="updateChartTimeRange('projectTime', $event)"
        >
          <v-chart :option="projectTimeOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 4. 专注度趋势 -->
        <ChartCard
          title="专注度趋势"
          :timeRange="charts.focusTrend.timeRange"
          @update:timeRange="updateChartTimeRange('focusTrend', $event)"
        >
          <v-chart :option="focusTrendOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 5. 时间热力图 -->
        <ChartCard
          title="时间热力图"
          :timeRange="charts.heatmap.timeRange"
          @update:timeRange="updateChartTimeRange('heatmap', $event)"
          class="lg:col-span-2"
        >
          <v-chart :option="heatmapOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 6. 收支趋势 -->
        <ChartCard
          title="收支趋势"
          :timeRange="charts.finance.timeRange"
          @update:timeRange="updateChartTimeRange('finance', $event)"
        >
          <v-chart :option="financeOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 7. 分类支出占比 -->
        <ChartCard
          title="支出分类占比"
          :timeRange="charts.expenseCategory.timeRange"
          @update:timeRange="updateChartTimeRange('expenseCategory', $event)"
        >
          <v-chart :option="expenseCategoryOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 8. 每日时间分布 -->
        <ChartCard
          title="每日时间分布"
          :timeRange="charts.dailyDistribution.timeRange"
          @update:timeRange="updateChartTimeRange('dailyDistribution', $event)"
        >
          <v-chart :option="dailyDistributionOption" autoresize class="h-80" />
        </ChartCard>
        
        <!-- 9. 优先级分布 -->
        <ChartCard
          title="计划优先级分布"
          :timeRange="charts.priorityDistribution.timeRange"
          @update:timeRange="updateChartTimeRange('priorityDistribution', $event)"
        >
          <v-chart :option="priorityDistributionOption" autoresize class="h-80" />
        </ChartCard>
      </div>
    </div>
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { 
  BarChart, LineChart, PieChart, HeatmapChart, 
  RadarChart, ScatterChart 
} from 'echarts/charts'
import {
  GridComponent, TooltipComponent, LegendComponent,
  TitleComponent, VisualMapComponent, CalendarComponent,
  DataZoomComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { Clock, Target, TrendingUp, Wallet } from 'lucide-vue-next'
import BaseCard from '@/components/common/BaseCard.vue'
import ChartCard from '@/components/statistics/ChartCard.vue'
import ErrorBoundary from '@/components/common/ErrorBoundary.vue'
import { formatDuration, formatCurrency, safeToFixed } from '@/utils/helpers'
import { handleApiError } from '@/utils/errorHandler'

// Register ECharts components
use([
  CanvasRenderer,
  BarChart, LineChart, PieChart, HeatmapChart, RadarChart, ScatterChart,
  GridComponent, TooltipComponent, LegendComponent, TitleComponent,
  VisualMapComponent, CalendarComponent, DataZoomComponent
])

// State
const globalTimeRange = ref('month')
const customStartDate = ref('')
const customEndDate = ref('')

const overview = ref({
  total_duration: 0,
  session_count: 0,
  completed_plans: 0,
  total_plans: 0,
  avg_focus_score: 0,
  total_income: 0,
  total_expense: 0,
  net_worth: 0
})

const charts = ref({
  timeTrend: { timeRange: 'month', data: [] },
  planCompletion: { timeRange: 'month', data: [] },
  projectTime: { timeRange: 'month', data: [] },
  focusTrend: { timeRange: 'month', data: [] },
  heatmap: { timeRange: 'year', data: [] },
  finance: { timeRange: 'month', data: [] },
  expenseCategory: { timeRange: 'month', data: [] },
  dailyDistribution: { timeRange: 'week', data: [] },
  priorityDistribution: { timeRange: 'month', data: [] }
})

// Chart Options
const timeTrendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['专注时长', '完成计划'] },
  xAxis: {
    type: 'category',
    data: charts.value.timeTrend.data.map((d: any) => d.date)
  },
  yAxis: [
    { type: 'value', name: '时长(小时)' },
    { type: 'value', name: '计划数' }
  ],
  series: [
    {
      name: '专注时长',
      type: 'bar',
      data: charts.value.timeTrend.data.map((d: any) => (d.duration / 3600).toFixed(1)),
      itemStyle: { color: '#3b82f6' }
    },
    {
      name: '完成计划',
      type: 'line',
      yAxisIndex: 1,
      data: charts.value.timeTrend.data.map((d: any) => d.completed_plans),
      itemStyle: { color: '#10b981' }
    }
  ]
}))

const planCompletionOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', left: 'left' },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: {
      borderRadius: 10,
      borderColor: '#fff',
      borderWidth: 2
    },
    label: { show: true, formatter: '{b}: {d}%' },
    data: charts.value.planCompletion.data
  }]
}))

const projectTimeOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  xAxis: {
    type: 'category',
    data: charts.value.projectTime.data.map((d: any) => d.name),
    axisLabel: { rotate: 30, interval: 0 }
  },
  yAxis: { type: 'value', name: '时长(小时)' },
  series: [{
    type: 'bar',
    data: charts.value.projectTime.data.map((d: any) => ({
      value: (d.duration / 3600).toFixed(1),
      itemStyle: { color: d.color || '#3b82f6' }
    })),
    barWidth: '60%'
  }]
}))

const focusTrendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: {
    type: 'category',
    data: charts.value.focusTrend.data.map((d: any) => d.date)
  },
  yAxis: { type: 'value', name: '专注度', max: 100 },
  series: [{
    type: 'line',
    data: charts.value.focusTrend.data.map((d: any) => d.focus_score),
    smooth: true,
    areaStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
          { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
        ]
      }
    },
    itemStyle: { color: '#3b82f6' }
  }]
}))

const heatmapOption = computed(() => ({
  tooltip: {
    formatter: (params: any) => `${params.data[0]}: ${params.data[1]}小时`
  },
  visualMap: {
    min: 0,
    max: 8,
    calculable: true,
    orient: 'horizontal',
    left: 'center',
    bottom: 20,
    inRange: {
      color: ['#e5e7eb', '#93c5fd', '#3b82f6', '#1d4ed8', '#1e3a8a']
    }
  },
  calendar: {
    range: getCalendarRange(),
    cellSize: ['auto', 20],
    top: 60,
    left: 80,
    right: 40
  },
  series: [{
    type: 'heatmap',
    coordinateSystem: 'calendar',
    data: charts.value.heatmap.data.map((d: any) => [
      d.date,
      (d.duration / 3600).toFixed(1)
    ])
  }]
}))

const financeOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['收入', '支出', '结余'] },
  xAxis: {
    type: 'category',
    data: charts.value.finance.data.map((d: any) => d.date)
  },
  yAxis: { type: 'value', name: '金额(元)' },
  series: [
    {
      name: '收入',
      type: 'line',
      data: charts.value.finance.data.map((d: any) => d.income),
      itemStyle: { color: '#10b981' },
      smooth: true
    },
    {
      name: '支出',
      type: 'line',
      data: charts.value.finance.data.map((d: any) => d.expense),
      itemStyle: { color: '#ef4444' },
      smooth: true
    },
    {
      name: '结余',
      type: 'bar',
      data: charts.value.finance.data.map((d: any) => d.income - d.expense),
      itemStyle: { color: '#3b82f6' }
    }
  ]
}))

const expenseCategoryOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
  legend: { orient: 'vertical', right: 10, top: 'center' },
  series: [{
    type: 'pie',
    radius: '70%',
    center: ['40%', '50%'],
    data: charts.value.expenseCategory.data,
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
    }
  }]
}))

const dailyDistributionOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: { type: 'value', name: '时长(小时)' },
  series: [{
    type: 'bar',
    data: charts.value.dailyDistribution.data,
    itemStyle: {
      color: (params: any) => {
        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4']
        return colors[params.dataIndex % colors.length]
      }
    }
  }]
}))

const priorityDistributionOption = computed(() => ({
  tooltip: { trigger: 'item' },
  radar: {
    indicator: [
      { name: '紧急且重要', max: 100 },
      { name: '重要不紧急', max: 100 },
      { name: '紧急不重要', max: 100 },
      { name: '不紧急不重要', max: 100 }
    ]
  },
  series: [{
    type: 'radar',
    data: [{
      value: charts.value.priorityDistribution.data,
      name: '计划分布',
      areaStyle: { color: 'rgba(59, 130, 246, 0.3)' },
      itemStyle: { color: '#3b82f6' }
    }]
  }]
}))

// Methods
const getCalendarRange = () => {
  const range = charts.value.heatmap.timeRange
  const now = new Date()
  
  if (range === 'year') {
    return now.getFullYear()
  } else if (range === 'month') {
    const year = now.getFullYear()
    const month = now.getMonth() + 1
    return `${year}-${month.toString().padStart(2, '0')}`
  }
  
  return now.getFullYear()
}

const onGlobalTimeRangeChange = () => {
  // 更新所有图表的时间范围
  Object.keys(charts.value).forEach(key => {
    charts.value[key as keyof typeof charts.value].timeRange = globalTimeRange.value
  })
  loadAllData()
}

const onCustomDateChange = () => {
  if (customStartDate.value && customEndDate.value) {
    loadAllData()
  }
}

const updateChartTimeRange = (chartKey: string, timeRange: string) => {
  charts.value[chartKey as keyof typeof charts.value].timeRange = timeRange
  loadChartData(chartKey)
}

const getDateRange = (timeRange: string) => {
  const now = new Date()
  let startDate, endDate
  
  switch (timeRange) {
    case 'today':
      startDate = endDate = now.toISOString().split('T')[0]
      break
    case 'week':
      const weekStart = new Date(now)
      weekStart.setDate(now.getDate() - now.getDay())
      startDate = weekStart.toISOString().split('T')[0]
      endDate = now.toISOString().split('T')[0]
      break
    case 'month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0]
      endDate = now.toISOString().split('T')[0]
      break
    case 'year':
      startDate = `${now.getFullYear()}-01-01`
      endDate = now.toISOString().split('T')[0]
      break
    case 'custom':
      startDate = customStartDate.value
      endDate = customEndDate.value
      break
    default:
      startDate = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0]
      endDate = now.toISOString().split('T')[0]
  }
  
  return { startDate, endDate }
}

const loadAllData = async () => {
  await Promise.all([
    loadOverview(),
    ...Object.keys(charts.value).map(key => loadChartData(key))
  ])
}

const loadOverview = async () => {
  try {
    const { startDate, endDate } = getDateRange(globalTimeRange.value)
    const response = await fetch(
      `http://localhost:8000/api/v1/statistics/overview?start_date=${startDate}&end_date=${endDate}`
    )
    if (response.ok) {
      overview.value = await response.json()
    }
  } catch (error) {
    handleApiError(error, '加载概览数据')
  }
}

const loadChartData = async (chartKey: string) => {
  try {
    const chart = charts.value[chartKey as keyof typeof charts.value]
    const { startDate, endDate } = getDateRange(chart.timeRange)
    
    const endpoints: Record<string, string> = {
      timeTrend: 'time-trend',
      planCompletion: 'plan-completion',
      projectTime: 'project-time',
      focusTrend: 'focus-trend',
      heatmap: 'heatmap',
      finance: 'finance-trend',
      expenseCategory: 'expense-category',
      dailyDistribution: 'daily-distribution',
      priorityDistribution: 'priority-distribution'
    }
    
    const endpoint = endpoints[chartKey]
    if (!endpoint) return
    
    const response = await fetch(
      `http://localhost:8000/api/v1/statistics/${endpoint}?start_date=${startDate}&end_date=${endDate}`
    )
    
    if (response.ok) {
      chart.data = await response.json()
    }
  } catch (error) {
    console.error(`Failed to load ${chartKey}:`, error)
  }
}

onMounted(() => {
  loadAllData()
})
</script>
