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
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态管理
const isLoginMode = ref(true) // 默认是登录模式，false 则是注册模式
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

// 切换登录/注册模式
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
      // ==========================================
      // 【模式 A：登录】必须按 OAuth2 标准打包成 Form 表单
      // ==========================================
      const params = new URLSearchParams()
      params.append('username', username.value)
      params.append('password', password.value)

      const response = await axios.post('http://127.0.0.1:8000/api/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })

      const token = response.data.access_token
      localStorage.setItem('token', token)
      router.push('/chat') // 登录成功，进大厅
      
    } else {
      // ==========================================
      // 【模式 B：注册】普通 API 接口，直接发 JSON 即可
      // ==========================================
      const response = await axios.post('http://127.0.0.1:8000/api/auth/register', {
        username: username.value,
        password: password.value
      })
      
      // 注册成功后，绿字提示用户，并自动切回登录页面让他登录
      successMessage.value = response.data.msg
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