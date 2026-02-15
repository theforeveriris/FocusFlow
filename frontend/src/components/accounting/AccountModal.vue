<template>
  <BaseModal v-model="isOpen" :title="isEdit ? '编辑账户' : '新建账户'" size="lg">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Account Name -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          账户名称 <span class="text-red-500">*</span>
        </label>
        <input
          v-model="formData.name"
          type="text"
          required
          placeholder="如：工商银行储蓄卡"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      
      <!-- Account Type -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            账户类型 <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.type"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="asset">资产账户</option>
            <option value="liability">负债账户</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            子类型
          </label>
          <select
            v-model="formData.sub_type"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">选择类型</option>
            <optgroup v-if="formData.type === 'asset'" label="资产类型">
              <option value="cash">现金</option>
              <option value="bank_card">银行卡</option>
              <option value="wechat">微信支付</option>
              <option value="alipay">支付宝</option>
            </optgroup>
            <optgroup v-if="formData.type === 'liability'" label="负债类型">
              <option value="credit_card">信用卡</option>
              <option value="bnpl">先用后付</option>
              <option value="loan">贷款</option>
            </optgroup>
          </select>
        </div>
      </div>
      
      <!-- Initial Balance & Credit Limit -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            初始余额 <span class="text-red-500">*</span>
          </label>
          <input
            v-model.number="formData.initial_balance"
            type="number"
            step="0.01"
            required
            placeholder="0.00"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ formData.type === 'liability' ? '负债账户初始余额通常为0或负数' : '资产账户的起始金额' }}
          </p>
        </div>
        
        <div v-if="formData.type === 'liability'">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            信用额度
          </label>
          <input
            v-model.number="formData.credit_limit"
            type="number"
            step="0.01"
            placeholder="0.00"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
          <p class="text-xs text-gray-500 mt-1">信用卡的最大可用额度</p>
        </div>
      </div>
      
      <!-- Icon & Color -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">图标</label>
          <select
            v-model="formData.icon"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="wallet">钱包</option>
            <option value="building-2">银行</option>
            <option value="message-circle">微信</option>
            <option value="smartphone">支付宝</option>
            <option value="credit-card">信用卡</option>
            <option value="shopping-bag">购物</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">颜色</label>
          <div class="flex gap-2">
            <input
              v-model="formData.color"
              type="color"
              class="w-12 h-10 border border-gray-300 rounded cursor-pointer"
            />
            <input
              v-model="formData.color"
              type="text"
              placeholder="#3b82f6"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>
      </div>
      
      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
        <textarea
          v-model="formData.description"
          rows="3"
          placeholder="账户备注信息"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      
      <!-- Settings -->
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-2 cursor-pointer">
          <input
            v-model="formData.is_active"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span class="text-sm text-gray-700">启用账户</span>
        </label>
        
        <label class="flex items-center gap-2 cursor-pointer">
          <input
            v-model="formData.is_default"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span class="text-sm text-gray-700">设为默认账户</span>
        </label>
      </div>
      
      <!-- Actions -->
      <div class="flex justify-end gap-2 pt-4 border-t">
        <BaseButton type="button" variant="outline" @click="isOpen = false">
          取消
        </BaseButton>
        <BaseButton type="submit" :loading="loading">
          {{ isEdit ? '保存' : '创建' }}
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseButton from '@/components/common/BaseButton.vue'

interface Account {
  id?: number
  name: string
  type: 'asset' | 'liability'
  sub_type?: string
  initial_balance: number
  credit_limit?: number
  icon?: string
  color?: string
  description?: string
  is_active: boolean
  is_default: boolean
}

const props = defineProps<{
  modelValue: boolean
  account?: Account | null
  loading?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'save': [data: Account]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.account?.id)

const defaultFormData: Account = {
  name: '',
  type: 'asset',
  sub_type: '',
  initial_balance: 0,
  credit_limit: undefined,
  icon: 'wallet',
  color: '#3b82f6',
  description: '',
  is_active: true,
  is_default: false
}

const formData = ref<Account>({ ...defaultFormData })

watch(() => props.account, (account) => {
  if (account) {
    formData.value = { ...account }
  } else {
    formData.value = { ...defaultFormData }
  }
}, { immediate: true })

watch(() => props.modelValue, (value) => {
  if (!value) {
    setTimeout(() => {
      formData.value = { ...defaultFormData }
    }, 300)
  }
})

const handleSubmit = () => {
  emit('save', { ...formData.value })
}
</script>
