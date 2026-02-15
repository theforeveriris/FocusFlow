import { defineStore } from 'pinia'
import { ref } from 'vue'
import { accountApi } from '@/api/accounts'

export interface Account {
  id: number
  name: string
  type: 'asset' | 'liability'
  sub_type?: string
  balance: number
  initial_balance: number
  credit_limit?: number
  icon?: string
  color?: string
  description?: string
  is_active: boolean
  is_default: boolean
  available_balance: number
  created_at: string
  updated_at: string
}

export interface AccountSummary {
  total_assets: number
  total_liabilities: number
  net_worth: number
  asset_accounts: Account[]
  liability_accounts: Account[]
}

export const useAccountStore = defineStore('accounts', () => {
  const accounts = ref<Account[]>([])
  const summary = ref<AccountSummary | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchAccounts = async (params?: { type?: string; is_active?: boolean }) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountApi.getAll(params)
      accounts.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch accounts'
    } finally {
      loading.value = false
    }
  }

  const fetchSummary = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await accountApi.getSummary()
      summary.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch summary'
    } finally {
      loading.value = false
    }
  }

  const createAccount = async (data: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountApi.create(data)
      accounts.value.push(response.data)
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create account'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateAccount = async (id: number, data: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountApi.update(id, data)
      const index = accounts.value.findIndex(a => a.id === id)
      if (index !== -1) {
        accounts.value[index] = response.data
      }
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update account'
      return null
    } finally {
      loading.value = false
    }
  }

  const deleteAccount = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await accountApi.delete(id)
      accounts.value = accounts.value.filter(a => a.id !== id)
      await fetchSummary()
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete account'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    accounts,
    summary,
    loading,
    error,
    fetchAccounts,
    fetchSummary,
    createAccount,
    updateAccount,
    deleteAccount
  }
})
