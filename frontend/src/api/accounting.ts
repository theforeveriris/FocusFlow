import api from './index'
import type { Transaction, Category, FinanceSummary } from '@/types'

export interface TransactionCreate {
  type: 'income' | 'expense'
  amount: number
  category_id?: number
  account_id?: number
  plan_id?: number
  project_id?: number
  transaction_date: string
  description?: string
  tags?: string[]
}

export interface CategoryCreate {
  name: string
  type: 'income' | 'expense'
  icon?: string
  color?: string
  parent_id?: number
  budget_limit?: number
}

export const accountingApi = {
  // Categories
  getCategories: (type?: 'income' | 'expense') =>
    api.get<Category[]>('/accounting/categories', { params: { type } }),

  createCategory: (data: CategoryCreate) =>
    api.post<Category>('/accounting/categories', data),

  // Transactions
  getTransactions: (params?: {
    type?: 'income' | 'expense' | 'transfer' | 'repayment'
    category_id?: number
    account_id?: number
    start_date?: string
    end_date?: string
  }) =>
    api.get<Transaction[]>('/accounting/transactions', { params }),

  getTransactionById: (id: number) =>
    api.get<Transaction>(`/accounting/transactions/${id}`),

  createTransaction: (data: TransactionCreate) =>
    api.post<Transaction>('/accounting/transactions', data),

  updateTransaction: (id: number, data: Partial<TransactionCreate>) =>
    api.put<Transaction>(`/accounting/transactions/${id}`, data),

  deleteTransaction: (id: number) =>
    api.delete(`/accounting/transactions/${id}`),

  // Summary
  getSummary: (params?: { start_date?: string; end_date?: string }) =>
    api.get<FinanceSummary>('/accounting/summary', { params })
}
