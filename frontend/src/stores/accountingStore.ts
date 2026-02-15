import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { accountingApi } from '@/api/accounting'
import type { Transaction, Category, FinanceSummary } from '@/types'

export const useAccountingStore = defineStore('accounting', () => {
  // State
  const transactions = ref<Transaction[]>([])
  const categories = ref<Category[]>([])
  const summary = ref<FinanceSummary>({
    total_income: 0,
    total_expense: 0,
    balance: 0,
    period: 'all time'
  })
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const incomeCategories = computed(() => categories.value.filter(c => c.type === 'income'))
  const expenseCategories = computed(() => categories.value.filter(c => c.type === 'expense'))
  
  const incomeTransactions = computed(() => transactions.value.filter(t => t.type === 'income'))
  const expenseTransactions = computed(() => transactions.value.filter(t => t.type === 'expense'))
  
  const totalIncome = computed(() => incomeTransactions.value.reduce((sum, t) => sum + t.amount, 0))
  const totalExpense = computed(() => expenseTransactions.value.reduce((sum, t) => sum + t.amount, 0))
  const balance = computed(() => totalIncome.value - totalExpense.value)

  const transactionsByDate = computed(() => {
    const grouped: Record<string, Transaction[]> = {}
    transactions.value.forEach(t => {
      const date = t.transaction_date
      if (!grouped[date]) {
        grouped[date] = []
      }
      grouped[date].push(t)
    })
    return grouped
  })

  // Actions
  const fetchCategories = async (type?: 'income' | 'expense') => {
    loading.value = true
    try {
      const response = await accountingApi.getCategories(type)
      categories.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch categories'
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (data: { name: string; type: 'income' | 'expense'; icon?: string; color?: string }) => {
    loading.value = true
    try {
      const response = await accountingApi.createCategory(data)
      categories.value.push(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create category'
      return null
    } finally {
      loading.value = false
    }
  }

  const fetchTransactions = async (params?: {
    type?: 'income' | 'expense' | 'transfer' | 'repayment'
    category_id?: number
    account_id?: number
    start_date?: string
    end_date?: string
  }) => {
    loading.value = true
    try {
      const response = await accountingApi.getTransactions(params)
      transactions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch transactions'
    } finally {
      loading.value = false
    }
  }

  const createTransaction = async (data: {
    type: 'income' | 'expense' | 'transfer' | 'repayment'
    amount: number
    category_id?: number
    from_account_id?: number
    to_account_id?: number
    transaction_date: string
    description?: string
    tags?: string[]
  }) => {
    loading.value = true
    try {
      const response = await accountingApi.createTransaction(data)
      transactions.value.unshift(response.data)
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create transaction'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateTransaction = async (id: number, data: Partial<{
    type: 'income' | 'expense'
    amount: number
    category_id?: number
    transaction_date: string
    description?: string
    tags?: string[]
  }>) => {
    loading.value = true
    try {
      const response = await accountingApi.updateTransaction(id, data)
      const index = transactions.value.findIndex(t => t.id === id)
      if (index !== -1) {
        transactions.value[index] = response.data
      }
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update transaction'
      return null
    } finally {
      loading.value = false
    }
  }

  const deleteTransaction = async (id: number) => {
    loading.value = true
    try {
      await accountingApi.deleteTransaction(id)
      transactions.value = transactions.value.filter(t => t.id !== id)
      await fetchSummary()
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete transaction'
      return false
    } finally {
      loading.value = false
    }
  }

  const fetchSummary = async (params?: { start_date?: string; end_date?: string }) => {
    try {
      const response = await accountingApi.getSummary(params)
      summary.value = response.data
    } catch (err: any) {
      console.error('Failed to fetch summary:', err)
    }
  }

  return {
    transactions,
    categories,
    summary,
    loading,
    error,
    incomeCategories,
    expenseCategories,
    incomeTransactions,
    expenseTransactions,
    totalIncome,
    totalExpense,
    balance,
    transactionsByDate,
    fetchCategories,
    createCategory,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    fetchSummary
  }
})
