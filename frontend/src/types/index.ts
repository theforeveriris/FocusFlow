// Plan types
export interface Plan {
  id: number
  title: string
  description?: string
  parent_id?: number
  project_id?: number
  project_name?: string
  priority_matrix: 'urgent_important' | 'not_urgent_important' | 'urgent_not_important' | 'not_urgent_not_important'
  status: 'todo' | 'in_progress' | 'completed' | 'cancelled'
  start_time?: string
  end_time?: string
  estimated_duration?: number
  actual_duration: number
  tags: string[]
  children_count: number
  created_at: string
  updated_at: string
}

export interface PlanCreate {
  title: string
  description?: string
  parent_id?: number
  project_id?: number
  priority_matrix?: string
  status?: string
  start_time?: string
  end_time?: string
  estimated_duration?: number
  tags?: string[]
}

// Project types
export interface Project {
  id: number
  name: string
  description?: string
  color: string
  icon?: string
  status: 'active' | 'archived' | 'deleted'
  start_date?: string
  end_date?: string
  progress: number
  plan_count: number
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
  color?: string
  icon?: string
  start_date?: string
  end_date?: string
}

// Timer types
export interface TimerSession {
  id: number
  plan_id?: number
  project_id?: number
  plan_title?: string
  project_name?: string
  start_time: string
  end_time?: string
  duration: number
  interrupt_count: number
  focus_score?: number
  notes?: string
  is_zen_mode: boolean
  created_at: string
}

export interface TimerTodayStats {
  total_duration: number
  session_count: number
  focus_score_avg?: number
}

// Accounting types
export interface Category {
  id: number
  name: string
  type: 'income' | 'expense'
  icon?: string
  color?: string
  parent_id?: number
  budget_limit?: number
  created_at: string
}

export interface Transaction {
  id: number
  type: 'income' | 'expense' | 'transfer' | 'repayment'
  amount: number
  category_id?: number
  category_name?: string
  category_icon?: string
  category_color?: string
  from_account_id?: number
  to_account_id?: number
  from_account_name?: string
  to_account_name?: string
  plan_id?: number
  project_id?: number
  transaction_date: string
  description?: string
  tags: string[]
  created_at: string
  updated_at: string
}

export interface FinanceSummary {
  total_income: number
  total_expense: number
  balance: number
  period: string
}

// Statistics types
export interface ProjectStats {
  id: number
  name: string
  color: string
  total_duration: number
  session_count: number
}

export interface HeatmapData {
  date: string
  duration: number
  level: number
}

export interface EfficiencyData {
  date: string
  focus_score: number
  duration: number
  interrupts: number
}

export interface MonthlyFinance {
  month: number
  income: number
  expense: number
  balance: number
}

// Navigation types
export interface NavItem {
  name: string
  path: string
  icon: string
}
