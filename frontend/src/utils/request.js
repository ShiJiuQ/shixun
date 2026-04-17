import axios from 'axios'

// 1. 从 Vite 环境变量中读取后端地址，如果没有就用本地兜底
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// 2. 创建 Axios 实例
const request = axios.create({
  baseURL: baseURL,
  timeout: 30000
})

// 3. 请求拦截器：出门前自动带上“通行证”
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// 4. 响应拦截器：回家时自动检查“有没有被保安拦下”
request.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.response && error.response.status === 401) {
    console.warn('Token 过期或无效，请重新登录')
    localStorage.removeItem('token') // 清除假死 token
    // 强制跳转回登录页 (如果用 vue-router 可以换成 router.push)
    window.location.href = '/login' 
  }
  return Promise.reject(error)
})

export default request