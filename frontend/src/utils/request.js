import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('token') // 🚀 必须与存储一致
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => Promise.reject(error))

// 响应拦截器
request.interceptors.response.use((response) => response, (error) => {
  if (error.response && error.response.status === 401) {
    sessionStorage.clear() // 清空会话
    window.location.href = '/login'
  }
  return Promise.reject(error)
})

export default request