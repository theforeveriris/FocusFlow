<template>
  <!-- Loading State -->
  <div v-if="isLoading" class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      <p class="text-gray-600">加载中...</p>
    </div>
  </div>
  
  <!-- Error State -->
  <div v-else-if="loadError" class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <div class="text-red-500 text-5xl mb-4">⚠️</div>
      <p class="text-gray-700 mb-4">{{ loadError }}</p>
      <BaseButton @click="location.reload()">刷新页面</BaseButton>
    </div>
  </div>
  
  <!-- Main Content -->
  <div v-else class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">记账管理</h1>
        <p class="text-gray-500 mt-1">管理你的账户和交易</p>
      </div>
      <div class="flex gap-2">
        <BaseButton @click="showAccountModal = true" variant="outline">
          <Plus class="w-4 h-4" />
          新建账户
        </BaseButton>
        <BaseButton @click="showTransactionModal = true">
          <Plus class="w-4 h-4" />
          记一笔
        </BaseButton>
      </div>
    </div>
    
    <!-- Financial Summary -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <BaseCard class="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-green-600 font-medium">总资产</div>
            <div class="text-3xl font-bold text-green-700 mt-1">
              ¥{{ formatNumber(accountSummary?.total_assets || 0) }}
            </div>
          </div>
          <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
            <TrendingUp class="w-6 h-6 text-white" />
          </div>
        </div>
      </BaseCard>
      
      <BaseCard class="bg-gradient-to-br from-red-50 to-red-100 border-red-200">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-red-600 font-medium">总负债</div>
            <div class="text-3xl font-bold text-red-700 mt-1">
              ¥{{ formatNumber(accountSummary?.total_liabilities || 0) }}
            </div>
          </div>
          <div class="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center">
            <TrendingDown class="w-6 h-6 text-white" />
          </div>
        </div>
      </BaseCard>
      
      <BaseCard class="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-blue-600 font-medium">净资产</div>
            <div class="text-3xl font-bold text-blue-700 mt-1">
              ¥{{ formatNumber(accountSummary?.net_worth || 0) }}
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
            <Wallet class="w-6 h-6 text-white" />
          </div>
        </div>
      </BaseCard>
    </div>
    
    <!-- Asset Accounts -->
    <BaseCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <Wallet class="w-5 h-5 text-green-600" />
            <h3 class="font-semibold text-gray-900">资产账户</h3>
            <span class="text-sm text-gray-500">({{ assetAccounts.length }})</span>
          </div>
        </div>
      </template>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="account in assetAccounts"
          :key="account.id"
          class="p-4 border-2 rounded-lg hover:shadow-md transition-all cursor-pointer"
          :style="{ borderColor: account.color || '#3b82f6' }"
          @click="selectAccount(account)"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-2">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :style="{ backgroundColor: (account.color || '#3b82f6') + '20' }"
              >
                <component 
                  :is="getAccountIcon(account.icon)" 
                  class="w-5 h-5"
                  :style="{ color: account.color || '#3b82f6' }"
                />
              </div>
              <div>
                <div class="font-medium text-gray-900">{{ account.name }}</div>
                <div class="text-xs text-gray-500">{{ getAccountTypeName(account.sub_type) }}</div>
              </div>
            </div>
            <button
              @click.stop="editAccount(account)"
              class="p-1 text-gray-400 hover:text-gray-600"
            >
              <Settings class="w-4 h-4" />
            </button>
          </div>
          
          <div class="space-y-1">
            <div class="flex items-baseline justify-between">
              <span class="text-xs text-gray-500">余额</span>
              <span class="text-lg font-bold text-gray-900">
                ¥{{ formatNumber(account.balance) }}
              </span>
            </div>
            <div class="flex items-baseline justify-between">
              <span class="text-xs text-gray-500">可用</span>
              <span class="text-sm text-green-600">
                ¥{{ formatNumber(account.available_balance) }}
              </span>
            </div>
          </div>
        </div>
        
        <div
          v-if="assetAccounts.length === 0"
          class="col-span-full text-center py-8 text-gray-500"
        >
          暂无资产账户，点击右上角添加
        </div>
      </div>
    </BaseCard>
    
    <!-- Liability Accounts -->
    <BaseCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <CreditCard class="w-5 h-5 text-red-600" />
            <h3 class="font-semibold text-gray-900">负债账户</h3>
            <span class="text-sm text-gray-500">({{ liabilityAccounts.length }})</span>
          </div>
        </div>
      </template>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="account in liabilityAccounts"
          :key="account.id"
          class="p-4 border-2 rounded-lg hover:shadow-md transition-all cursor-pointer"
          :style="{ borderColor: account.color || '#ef4444' }"
          @click="selectAccount(account)"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-2">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :style="{ backgroundColor: (account.color || '#ef4444') + '20' }"
              >
                <component 
                  :is="getAccountIcon(account.icon)" 
                  class="w-5 h-5"
                  :style="{ color: account.color || '#ef4444' }"
                />
              </div>
              <div>
                <div class="font-medium text-gray-900">{{ account.name }}</div>
                <div class="text-xs text-gray-500">{{ getAccountTypeName(account.sub_type) }}</div>
              </div>
            </div>
            <button
              @click.stop="editAccount(account)"
              class="p-1 text-gray-400 hover:text-gray-600"
            >
              <Settings class="w-4 h-4" />
            </button>
          </div>
          
          <div class="space-y-1">
            <div class="flex items-baseline justify-between">
              <span class="text-xs text-gray-500">欠款</span>
              <span class="text-lg font-bold text-red-600">
                ¥{{ formatNumber(Math.abs(account.balance)) }}
              </span>
            </div>
            <div v-if="account.credit_limit" class="flex items-baseline justify-between">
              <span class="text-xs text-gray-500">额度</span>
              <span class="text-sm text-gray-600">
                ¥{{ formatNumber(account.credit_limit) }}
              </span>
            </div>
            <div v-if="account.credit_limit" class="flex items-baseline justify-between">
              <span class="text-xs text-gray-500">可用</span>
              <span class="text-sm text-green-600">
                ¥{{ formatNumber(account.available_balance) }}
              </span>
            </div>
          </div>
        </div>
        
        <div
          v-if="liabilityAccounts.length === 0"
          class="col-span-full text-center py-8 text-gray-500"
        >
          暂无负债账户
        </div>
      </div>
    </BaseCard>
    
    <!-- Quick Transaction -->
    <BaseCard>
      <template #header>
        <h3 class="font-semibold text-gray-900">快速记账</h3>
      </template>
      
      <div class="space-y-4">
        <!-- Transaction Type -->
        <div class="flex gap-2">
          <button
            @click="quickTransaction.type = 'expense'"
            class="flex-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors"
            :class="quickTransaction.type === 'expense' ? 'bg-red-50 border-red-500 text-red-600' : 'border-gray-200 text-gray-600'"
          >
            支出
          </button>
          <button
            @click="quickTransaction.type = 'income'"
            class="flex-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors"
            :class="quickTransaction.type === 'income' ? 'bg-green-50 border-green-500 text-green-600' : 'border-gray-200 text-gray-600'"
          >
            收入
          </button>
          <button
            @click="quickTransaction.type = 'transfer'"
            class="flex-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors"
            :class="quickTransaction.type === 'transfer' ? 'bg-blue-50 border-blue-500 text-blue-600' : 'border-gray-200 text-gray-600'"
          >
            转账
          </button>
          <button
            @click="quickTransaction.type = 'repayment'"
            class="flex-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors"
            :class="quickTransaction.type === 'repayment' ? 'bg-purple-50 border-purple-500 text-purple-600' : 'border-gray-200 text-gray-600'"
          >
            还款
          </button>
        </div>
        
        <!-- Form Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <input
            v-model="quickTransaction.amount"
            type="number"
            step="0.01"
            placeholder="金额"
            class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
          
          <!-- Income: to_account -->
          <select
            v-if="quickTransaction.type === 'income'"
            v-model="quickTransaction.to_account_id"
            class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          >
            <option value="">选择收入账户</option>
            <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
              {{ acc.name }}
            </option>
          </select>
          
          <!-- Expense: from_account -->
          <select
            v-if="quickTransaction.type === 'expense'"
            v-model="quickTransaction.from_account_id"
            class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          >
            <option value="">选择支出账户</option>
            <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
              {{ acc.name }} (¥{{ formatNumber(acc.balance) }})
            </option>
          </select>
          
          <!-- Transfer: from_account and to_account -->
          <template v-if="quickTransaction.type === 'transfer'">
            <select
              v-model="quickTransaction.from_account_id"
              class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
            >
              <option value="">从账户</option>
              <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }} (¥{{ formatNumber(acc.balance) }})
              </option>
            </select>
            <select
              v-model="quickTransaction.to_account_id"
              class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
            >
              <option value="">到账户</option>
              <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }}
              </option>
            </select>
          </template>
          
          <!-- Repayment: from_account (asset) and to_account (liability) -->
          <template v-if="quickTransaction.type === 'repayment'">
            <select
              v-model="quickTransaction.from_account_id"
              class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
            >
              <option value="">还款来源</option>
              <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }} (¥{{ formatNumber(acc.balance) }})
              </option>
            </select>
            <select
              v-model="quickTransaction.to_account_id"
              class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
            >
              <option value="">还款目标</option>
              <option v-for="acc in liabilityAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }} (欠¥{{ formatNumber(Math.abs(acc.balance)) }})
              </option>
            </select>
          </template>
          
          <!-- Category (only for income/expense) -->
          <select
            v-if="quickTransaction.type === 'income' || quickTransaction.type === 'expense'"
            v-model="quickTransaction.category_id"
            class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          >
            <option value="">选择分类(可选)</option>
            <option
              v-for="cat in filteredCategories"
              :key="cat.id"
              :value="cat.id"
            >
              {{ cat.name }}
            </option>
          </select>
          
          <input
            v-model="quickTransaction.description"
            type="text"
            placeholder="备注"
            class="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-100 focus:border-primary-500"
          />
          
          <BaseButton @click="addTransaction" :loading="loading" class="md:col-span-2 lg:col-span-1">
            <Plus class="w-4 h-4" />
            添加
          </BaseButton>
        </div>
      </div>
    </BaseCard>
    
    <!-- Transactions List -->
    <BaseCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">交易记录</h3>
          <div class="flex items-center gap-2">
            <select
              v-model="filterType"
              class="px-3 py-1.5 border border-gray-200 rounded-md text-sm"
            >
              <option value="">全部</option>
              <option value="income">收入</option>
              <option value="expense">支出</option>
            </select>
          </div>
        </div>
      </template>
      
      <div class="divide-y divide-gray-200">
        <div
          v-for="transaction in filteredTransactions"
          :key="transaction.id"
          class="py-4 flex items-center justify-between hover:bg-gray-50 -mx-4 px-4"
        >
          <div class="flex items-center gap-3">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center"
              :style="{ backgroundColor: transaction.category_color + '20' }"
            >
              <component 
                :is="getCategoryIcon(transaction.category_icon)" 
                class="w-5 h-5"
                :style="{ color: transaction.category_color }"
              />
            </div>
            <div>
              <div class="font-medium text-gray-900">
                {{ transaction.description || transaction.category_name || '未分类' }}
              </div>
              <div class="text-sm text-gray-500">
                {{ formatDate(transaction.transaction_date) }}
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-4">
            <div
              class="font-semibold"
              :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
            >
              {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
            </div>
            <button
              @click="deleteTransaction(transaction.id)"
              class="p-1.5 text-gray-400 hover:text-red-500 transition-colors"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div v-if="filteredTransactions.length === 0" class="py-8 text-center text-gray-500">
          暂无交易记录
        </div>
      </div>
    </BaseCard>
  </div>
  
  <!-- Account Modal -->
  <AccountModal
    v-model="showAccountModal"
    :account="editingAccount"
    :loading="loading"
    @save="saveAccount"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountingStore } from '@/stores/accountingStore'
import { useAccountStore } from '@/stores/accountStore'
import { 
  Plus, Trash2, ShoppingCart, Coffee, Car, Home, Briefcase, Gift, 
  TrendingUp, TrendingDown, Wallet, CreditCard, Settings,
  Building2, MessageCircle, Smartphone, ShoppingBag
} from 'lucide-vue-next'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AccountModal from '@/components/accounting/AccountModal.vue'
import { formatCurrency, formatDate } from '@/utils/helpers'

const router = useRouter()
const accountingStore = useAccountingStore()
const accountStore = useAccountStore()

// State
const showAccountModal = ref(false)
const showTransactionModal = ref(false)
const editingAccount = ref<any>(null)
const isLoading = ref(true)
const loadError = ref<string | null>(null)
const quickTransaction = ref({
  type: 'expense' as 'income' | 'expense' | 'transfer' | 'repayment',
  amount: '',
  category_id: '',
  from_account_id: '',
  to_account_id: '',
  description: '',
  transaction_date: new Date().toISOString().split('T')[0]
})
const filterType = ref('')

// Computed
const loading = computed(() => accountingStore.loading || accountStore.loading)
const categories = computed(() => accountingStore.categories)
const transactions = computed(() => accountingStore.transactions)
const summary = computed(() => accountingStore.summary)
const accountSummary = computed(() => accountStore.summary)

const assetAccounts = computed(() => accountSummary.value?.asset_accounts || [])
const liabilityAccounts = computed(() => accountSummary.value?.liability_accounts || [])

const filteredCategories = computed(() => {
  return categories.value.filter(c => c.type === quickTransaction.value.type)
})

const filteredTransactions = computed(() => {
  if (!filterType.value) return transactions.value
  return transactions.value.filter(t => t.type === filterType.value)
})

const formatNumber = (num: number) => {
  return num.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const iconMap: Record<string, any> = {
  'shopping-cart': ShoppingCart,
  'coffee': Coffee,
  'car': Car,
  'home': Home,
  'briefcase': Briefcase,
  'gift': Gift,
  'trending-up': TrendingUp,
  'wallet': Wallet,
  'building-2': Building2,
  'message-circle': MessageCircle,
  'smartphone': Smartphone,
  'credit-card': CreditCard,
  'shopping-bag': ShoppingBag
}

const getCategoryIcon = (iconName?: string) => {
  return iconMap[iconName || ''] || ShoppingCart
}

const getAccountIcon = (iconName?: string) => {
  return iconMap[iconName || ''] || Wallet
}

const getAccountTypeName = (subType?: string) => {
  const typeMap: Record<string, string> = {
    'cash': '现金',
    'bank_card': '银行卡',
    'wechat': '微信',
    'alipay': '支付宝',
    'credit_card': '信用卡',
    'bnpl': '先用后付',
    'loan': '贷款'
  }
  return typeMap[subType || ''] || '其他'
}

// Methods
onMounted(async () => {
  console.time('AccountingView Load')
  isLoading.value = true
  loadError.value = null
  
  try {
    // 并行执行所有 API 调用
    await Promise.all([
      accountingStore.fetchCategories(),
      accountingStore.fetchTransactions(),
      accountingStore.fetchSummary(),
      accountStore.fetchSummary()
    ])
    console.log('All data loaded successfully')
  } catch (error) {
    console.error('Failed to load accounting data:', error)
    loadError.value = '加载数据失败，请刷新页面重试'
  } finally {
    isLoading.value = false
    console.timeEnd('AccountingView Load')
  }
})

const selectAccount = (account: any) => {
  router.push(`/accounting/account/${account.id}`)
}

const editAccount = (account: any) => {
  editingAccount.value = account
  showAccountModal.value = true
}

const createAccount = () => {
  editingAccount.value = null
  showAccountModal.value = true
}

const saveAccount = async (data: any) => {
  if (editingAccount.value?.id) {
    await accountStore.updateAccount(editingAccount.value.id, data)
  } else {
    await accountStore.createAccount(data)
  }
  showAccountModal.value = false
  editingAccount.value = null
}

const deleteAccount = async (id: number) => {
  if (confirm('确定要删除这个账户吗？如果有交易记录，账户将被标记为不活跃。')) {
    await accountStore.deleteAccount(id)
  }
}

const addTransaction = async () => {
  if (!quickTransaction.value.amount) {
    alert('请填写金额')
    return
  }
  
  const data: any = {
    type: quickTransaction.value.type,
    amount: parseFloat(quickTransaction.value.amount),
    description: quickTransaction.value.description,
    transaction_date: quickTransaction.value.transaction_date,
    tags: []
  }
  
  if (quickTransaction.value.type === 'income') {
    if (!quickTransaction.value.to_account_id) {
      alert('请选择收入账户')
      return
    }
    data.to_account_id = parseInt(quickTransaction.value.to_account_id)
    data.category_id = quickTransaction.value.category_id ? parseInt(quickTransaction.value.category_id) : null
  } else if (quickTransaction.value.type === 'expense') {
    if (!quickTransaction.value.from_account_id) {
      alert('请选择支出账户')
      return
    }
    data.from_account_id = parseInt(quickTransaction.value.from_account_id)
    data.category_id = quickTransaction.value.category_id ? parseInt(quickTransaction.value.category_id) : null
  } else if (quickTransaction.value.type === 'transfer') {
    if (!quickTransaction.value.from_account_id || !quickTransaction.value.to_account_id) {
      alert('请选择转出和转入账户')
      return
    }
    data.from_account_id = parseInt(quickTransaction.value.from_account_id)
    data.to_account_id = parseInt(quickTransaction.value.to_account_id)
  } else if (quickTransaction.value.type === 'repayment') {
    if (!quickTransaction.value.from_account_id || !quickTransaction.value.to_account_id) {
      alert('请选择还款来源和还款目标')
      return
    }
    data.from_account_id = parseInt(quickTransaction.value.from_account_id)
    data.to_account_id = parseInt(quickTransaction.value.to_account_id)
  }
  
  await accountingStore.createTransaction(data)
  await accountStore.fetchSummary()
  
  // Reset form
  quickTransaction.value = {
    type: 'expense',
    amount: '',
    category_id: '',
    from_account_id: '',
    to_account_id: '',
    description: '',
    transaction_date: new Date().toISOString().split('T')[0]
  }
}

const deleteTransaction = async (id: number) => {
  if (confirm('确定要删除这条记录吗？')) {
    await accountingStore.deleteTransaction(id)
    await accountStore.fetchSummary()
  }
}
</script>
