import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1'

export const accountApi = {
  // 获取所有账户
  getAll: (params?: { type?: string; is_active?: boolean }) => 
    axios.get(`${API_BASE}/accounts`, { params }),
  
  // 获取账户汇总
  getSummary: () => 
    axios.get(`${API_BASE}/accounts/summary`),
  
  // 获取账户详情
  getById: (id: number) => 
    axios.get(`${API_BASE}/accounts/${id}`),
  
  // 创建账户
  create: (data: any) => 
    axios.post(`${API_BASE}/accounts`, data),
  
  // 更新账户
  update: (id: number, data: any) => 
    axios.put(`${API_BASE}/accounts/${id}`, data),
  
  // 删除账户
  delete: (id: number) => 
    axios.delete(`${API_BASE}/accounts/${id}`)
}
