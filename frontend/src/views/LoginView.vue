<template>
  <div class="login-container">
    <div class="login-box">
      <h2>{{ isLoginMode ? '研途 Buddy 登录' : '注册新账号' }}</h2>
      
      <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-msg">{{ successMessage }}</div>
      
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label>账号</label>
          <input type="text" v-model="username" placeholder="请输入账号" required />
        </div>
        
        <div class="input-group">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请输入密码" required />
        </div>
        
        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="isLoading">处理中...</span>
          <span v-else>{{ isLoginMode ? '登 录' : '注 册' }}</span>
        </button>
      </form>

      <div class="toggle-mode">
        <span v-if="isLoginMode">还没有账号？ <a href="#" @click.prevent="toggleMode">立即注册</a></span>
        <span v-else>已有账号？ <a href="#" @click.prevent="toggleMode">返回登录</a></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth.js' 

const router = useRouter()

// 状态管理
const isLoginMode = ref(true) 
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  errorMessage.value = ''
  successMessage.value = ''
}

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true
  
  try {
    if (isLoginMode.value) {
      const response = await authApi.login(username.value, password.value)
      
      // 🚀 1. 兼容获取 Token
      const token = response.data.access_token || response.data.token
      
      // 🚀 2. 必须改成 sessionStorage！并且把用户名也存下来给画像用
      sessionStorage.setItem('token', token)
      sessionStorage.setItem('username', username.value)
      
      // 🚀 3. 跳转到根路径 '/'，让路由守卫去分配到底去哪
      router.push('/') 
      
    } else {
      const response = await authApi.register(username.value, password.value)
      successMessage.value = response.data?.msg || '注册成功，请登录！' 
      isLoginMode.value = true 
    }
  } catch (error) {
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.detail || '发生错误'
    } else {
      errorMessage.value = '服务器连接失败，请检查后端是否开启'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 原有样式保持不变 */
.login-container { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f7fa; }
.login-box { width: 400px; padding: 40px; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
h2 { text-align: center; color: #333; margin-bottom: 24px; }
.input-group { margin-bottom: 20px; }
.input-group label { display: block; margin-bottom: 8px; color: #666; font-size: 14px; }
.input-group input { width: 100%; padding: 10px; border: 1px solid #dcdfe6; border-radius: 6px; box-sizing: border-box; }
.login-btn { width: 100%; padding: 12px; background-color: #409eff; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; transition: 0.3s; }
.login-btn:hover { background-color: #66b1ff; }
.login-btn:disabled { background-color: #a0cfff; cursor: not-allowed; }
.error-msg { color: #f56c6c; background-color: #fef0f0; padding: 10px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-size: 14px; }

/* 【新增】成功提示框 和 底部切换按钮的样式 */
.success-msg { color: #67c23a; background-color: #f0f9eb; padding: 10px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-size: 14px; }
.toggle-mode { margin-top: 20px; text-align: center; font-size: 14px; color: #606266; }
.toggle-mode a { color: #409eff; text-decoration: none; font-weight: bold; }
.toggle-mode a:hover { text-decoration: underline; }
</style>