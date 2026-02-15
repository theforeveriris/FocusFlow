<template>
  <!-- Loading State -->
  <div v-if="isPageLoading" class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      <p class="text-gray-600">加载账户信息...</p>
    </div>
  </div>
  
  <!-- Error State -->
  <div v-else-if="loadError || !account" class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <div class="text-red-500 text-5xl mb-4">⚠️</div>
      <p class="text-gray-700 mb-4">{{ loadError || '账户不存在' }}</p>
      <BaseButton @click="$router.push('/accounting')">返回记账页面</BaseButton>
    </div>
  </div>
  
  <!-- Main Content -->
  <div v-else class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <button
        @click="$router.back()"
        class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <ArrowLeft class="w-5 h-5" />
      </button>
      
      <div class="flex-1">
        <div class="flex items-center gap-3">
          <div 
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :style="{ backgroundColor: (account.color || '#3b82f6') + '20' }"
          >
            <component 
              :is="getAccountIcon(account.icon)" 
              class="w-6 h-6"
              :style="{ color: account.color || '#3b82f6' }"
            />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ account.name }}</h1>
            <p class="text-gray-500">{{ getAccountTypeName(account.sub_type) }}</p>
          </div>
        </div>
      </div>
      
      <div class="flex gap-2">
        <BaseButton @click="showTransactionModal = true">
          <Plus class="w-4 h-4" />
          记一笔
        </BaseButton>
        <BaseButton variant="outline" @click="editAccount">
          <Settings class="w-4 h-4" />
          设置
        </BaseButton>
      </div>
    </div>
    
    <!-- Account Info Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <BaseCard>
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">当前余额</div>
          <div 
            class="text-3xl font-bold"
            :class="account.type === 'asset' ? 'text-green-600' : 'text-red-600'"
          >
            ¥{{ formatNumber(account.type === 'asset' ? account.balance : Math.abs(account.balance)) }}
          </div>
          <div v-if="account.type === 'liability'" class="text-xs text-gray-500 mt-1">
            {{ account.balance < 0 ? '欠款' : '已还清' }}
          </div>
        </div>
      </BaseCard>
      
      <BaseCard v-if="account.credit_limit">
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">信用额度</div>
          <div class="text-3xl font-bold text-gray-900">
            ¥{{ formatNumber(account.credit_limit) }}
          </div>
        </div>
      </BaseCard>
      
      <BaseCard>
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">可用余额</div>
          <div class="text-3xl font-bold text-blue-600">
            ¥{{ formatNumber(account.available_balance) }}
          </div>
        </div>
      </BaseCard>
    </div>
    
    <!-- Quick Actions -->
    <BaseCard>
      <template #header>
        <h3 class="font-semibold text-gray-900">快速操作</h3>
      </template>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-if="account.type === 'asset'"
          @click="openQuickTransaction('expense')"
          class="p-4 border-2 border-gray-200 rounded-lg hover:border-red-500 hover:bg-red-50 transition-all group"
        >
          <ArrowDownCircle class="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-red-500" />
          <div class="text-sm font-medium text-gray-700 group-hover:text-red-600">支出</div>
        </button>
        
        <button
          v-if="account.type === 'asset'"
          @click="openQuickTransaction('income')"
          class="p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all group"
        >
          <ArrowUpCircle class="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-green-500" />
          <div class="text-sm font-medium text-gray-700 group-hover:text-green-600">收入</div>
        </button>
        
        <button
          @click="openQuickTransaction('transfer')"
          class="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all group"
        >
          <ArrowRightLeft class="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-blue-500" />
          <div class="text-sm font-medium text-gray-700 group-hover:text-blue-600">转账</div>
        </button>
        
        <button
          v-if="account.type === 'liability'"
          @click="openQuickTransaction('repayment')"
          class="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-all group"
        >
          <CreditCard class="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-purple-500" />
          <div class="text-sm font-medium text-gray-700 group-hover:text-purple-600">还款</div>
        </button>
      </div>
    </BaseCard>
    
    <!-- Transaction Form -->
    <BaseCard v-if="showTransactionForm">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">{{ getTransactionTitle() }}</h3>
          <button @click="showTransactionForm = false" class="text-gray-400 hover:text-gray-600">
            <X class="w-5 h-5" />
          </button>
        </div>
      </template>
      
      <form @submit.prevent="submitTransaction" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              金额 <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="transactionForm.amount"
              type="number"
              step="0.01"
              required
              placeholder="0.00"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          
          <!-- Account Selection based on transaction type -->
          <div v-if="transactionForm.type === 'transfer'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ account.type === 'asset' ? '转入账户' : '转出账户' }} <span class="text-red-500">*</span>
            </label>
            <select
              v-model="transactionForm.other_account_id"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">选择账户</option>
              <option v-for="acc in otherAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }} (¥{{ formatNumber(acc.balance) }})
              </option>
            </select>
          </div>
          
          <div v-if="transactionForm.type === 'repayment'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              还款来源 <span class="text-red-500">*</span>
            </label>
            <select
              v-model="transactionForm.other_account_id"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">选择账户</option>
              <option v-for="acc in assetAccounts" :key="acc.id" :value="acc.id">
                {{ acc.name }} (¥{{ formatNumber(acc.balance) }})
              </option>
            </select>
          </div>
          
          <div v-if="transactionForm.type === 'income' || transactionForm.type === 'expense'">
            <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
            <select
              v-model="transactionForm.category_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">选择分类(可选)</option>
              <option v-for="cat in filteredCategories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">备注</label>
          <input
            v-model="transactionForm.description"
            type="text"
            placeholder="交易备注"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
        
        <div class="flex justify-end gap-2">
          <BaseButton type="button" variant="outline" @click="showTransactionForm = false">
            取消
          </BaseButton>
          <BaseButton type="submit" :loading="loading">
            确认
          </BaseButton>
        </div>
      </form>
    </BaseCard>
    
    <!-- Transactions List -->
    <BaseCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">交易记录</h3>
          <select
            v-model="filterType"
            class="px-3 py-1.5 border border-gray-200 rounded-md text-sm"
          >
            <option value="">全部</option>
            <option value="income">收入</option>
            <option value="expense">支出</option>
            <option value="transfer">转账</option>
            <option value="repayment">还款</option>
          </select>
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
              :class="getTransactionColorClass(transaction.type)"
            >
              <component :is="getTransactionIcon(transaction.type)" class="w-5 h-5" />
            </div>
            <div>
              <div class="font-medium text-gray-900">
                {{ transaction.description || getTransactionTypeName(transaction.type) }}
              </div>
              <div class="text-sm text-gray-500">
                {{ formatDate(transaction.transaction_date) }}
                <span v-if="transaction.from_account_name || transaction.to_account_name" class="ml-2">
                  {{ getTransactionAccountInfo(transaction) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-4">
            <div
              class="font-semibold"
              :class="getAmountColorClass(transaction)"
            >
              {{ getAmountPrefix(transaction) }}¥{{ formatNumber(transaction.amount) }}
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accountStore'
import { useAccountingStore } from '@/stores/accountingStore'
import {
  ArrowLeft, Plus, Settings, ArrowDownCircle, ArrowUpCircle,
  ArrowRightLeft, CreditCard, X, Trash2,
  Wallet, Building2, MessageCircle, Smartphone, ShoppingBag
} from 'lucide-vue-next'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const accountingStore = useAccountingStore()

const accountId = computed(() => parseInt(route.params.id as string))
const account = ref<any>(null)
const showTransactionModal = ref(false)
const showTransactionForm = ref(false)
const filterType = ref('')
const loading = ref(false)
const isPageLoading = ref(true)
const loadError = ref<string | null>(null)

const transactionForm = ref({
  type: 'expense' as 'income' | 'expense' | 'transfer' | 'repayment',
  amount: 0,
  category_id: '',
  other_account_id: '',
  description: ''
})

const transactions = computed(() => accountingStore.transactions)
const categories = computed(() => accountingStore.categories)
const allAccounts = computed(() => accountStore.accounts)

const assetAccounts = computed(() => 
  allAccounts.value.filter(a => a.type === 'asset' && a.id !== accountId.value)
)

const otherAccounts = computed(() => 
  allAccounts.value.filter(a => a.id !== accountId.value)
)

const filteredCategories = computed(() => {
  return categories.value.filter(c => c.type === transactionForm.value.type)
})

const filteredTransactions = computed(() => {
  let result = transactions.value.filter(t => 
    t.from_account_id === accountId.value || t.to_account_id === accountId.value
  )
  
  if (filterType.value) {
    result = result.filter(t => t.type === filterType.value)
  }
  
  return result
})

const formatNumber = (num: number) => {
  return num.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const iconMap: Record<string, any> = {
  'wallet': Wallet,
  'building-2': Building2,
  'message-circle': MessageCircle,
  'smartphone': Smartphone,
  'credit-card': CreditCard,
  'shopping-bag': ShoppingBag
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

const getTransactionTitle = () => {
  const titles = {
    income: '记录收入',
    expense: '记录支出',
    transfer: '账户转账',
    repayment: '还款'
  }
  return titles[transactionForm.value.type]
}

const getTransactionIcon = (type: string) => {
  const icons = {
    income: ArrowUpCircle,
    expense: ArrowDownCircle,
    transfer: ArrowRightLeft,
    repayment: CreditCard
  }
  return icons[type as keyof typeof icons] || ArrowDownCircle
}

const getTransactionColorClass = (type: string) => {
  const classes = {
    income: 'bg-green-100 text-green-600',
    expense: 'bg-red-100 text-red-600',
    transfer: 'bg-blue-100 text-blue-600',
    repayment: 'bg-purple-100 text-purple-600'
  }
  return classes[type as keyof typeof classes] || 'bg-gray-100 text-gray-600'
}

const getTransactionTypeName = (type: string) => {
  const names = {
    income: '收入',
    expense: '支出',
    transfer: '转账',
    repayment: '还款'
  }
  return names[type as keyof typeof names] || type
}

const getTransactionAccountInfo = (transaction: any) => {
  if (transaction.type === 'transfer') {
    if (transaction.from_account_id === accountId.value) {
      return `转出到 ${transaction.to_account_name || '其他账户'}`
    } else {
      return `从 ${transaction.from_account_name || '其他账户'} 转入`
    }
  } else if (transaction.type === 'repayment') {
    if (transaction.from_account_id === accountId.value) {
      return `还款到 ${transaction.to_account_name || '负债账户'}`
    } else {
      return `从 ${transaction.from_account_name || '资产账户'} 还款`
    }
  }
  return ''
}

const getAmountColorClass = (transaction: any) => {
  // 判断是流入还是流出
  if (transaction.to_account_id === accountId.value) {
    return 'text-green-600' // 流入
  } else if (transaction.from_account_id === accountId.value) {
    return 'text-red-600' // 流出
  }
  return 'text-gray-600'
}

const getAmountPrefix = (transaction: any) => {
  if (transaction.to_account_id === accountId.value) {
    return '+' // 流入
  } else if (transaction.from_account_id === accountId.value) {
    return '-' // 流出
  }
  return ''
}

onMounted(async () => {
  console.time('AccountDetailView Load')
  isPageLoading.value = true
  loadError.value = null
  
  try {
    // 并行加载所有数据
    await Promise.all([
      loadAccount(),
      accountingStore.fetchCategories(),
      accountingStore.fetchTransactions({ account_id: accountId.value }),
      accountStore.fetchAccounts()
    ])
    console.log('Account detail loaded successfully')
  } catch (error) {
    console.error('Failed to load account detail:', error)
    loadError.value = '加载账户详情失败'
  } finally {
    isPageLoading.value = false
    console.timeEnd('AccountDetailView Load')
  }
})

const loadAccount = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/accounts/${accountId.value}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    account.value = data
  } catch (error) {
    console.error('Failed to load account:', error)
    alert('加载账户信息失败，返回记账页面')
    router.push('/accounting')
  }
}

const editAccount = () => {
  // TODO: Open edit modal
  console.log('Edit account')
}

const openQuickTransaction = (type: 'income' | 'expense' | 'transfer' | 'repayment') => {
  transactionForm.value = {
    type,
    amount: 0,
    category_id: '',
    other_account_id: '',
    description: ''
  }
  showTransactionForm.value = true
}

const submitTransaction = async () => {
  loading.value = true
  try {
    const data: any = {
      type: transactionForm.value.type,
      amount: transactionForm.value.amount,
      description: transactionForm.value.description,
      transaction_date: new Date().toISOString().split('T')[0],
      tags: []
    }
    
    if (transactionForm.value.type === 'income') {
      data.to_account_id = accountId.value
      if (transactionForm.value.category_id) {
        data.category_id = parseInt(transactionForm.value.category_id)
      }
    } else if (transactionForm.value.type === 'expense') {
      data.from_account_id = accountId.value
      if (transactionForm.value.category_id) {
        data.category_id = parseInt(transactionForm.value.category_id)
      }
    } else if (transactionForm.value.type === 'transfer') {
      if (account.value.type === 'asset') {
        data.from_account_id = accountId.value
        data.to_account_id = parseInt(transactionForm.value.other_account_id)
      } else {
        data.to_account_id = accountId.value
        data.from_account_id = parseInt(transactionForm.value.other_account_id)
      }
    } else if (transactionForm.value.type === 'repayment') {
      data.from_account_id = parseInt(transactionForm.value.other_account_id)
      data.to_account_id = accountId.value
    }
    
    await accountingStore.createTransaction(data)
    await loadAccount()
    await accountingStore.fetchTransactions({ account_id: accountId.value })
    
    showTransactionForm.value = false
    transactionForm.value = {
      type: 'expense',
      amount: 0,
      category_id: '',
      other_account_id: '',
      description: ''
    }
  } catch (error) {
    console.error('Failed to create transaction:', error)
    alert('创建交易失败')
  } finally {
    loading.value = false
  }
}

const deleteTransaction = async (id: number) => {
  if (confirm('确定要删除这条记录吗？')) {
    await accountingStore.deleteTransaction(id)
    await loadAccount()
    await accountingStore.fetchTransactions({ account_id: accountId.value })
  }
}
</script>
