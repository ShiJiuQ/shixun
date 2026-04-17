import request from '../utils/request' // 引入咱们封装好的请求工具

export const authApi = {
  /**
   * 登录接口
   * 🚨 注意：FastAPI 的 OAuth2 规范要求必须以表单 (x-www-form-urlencoded) 格式提交
   */
  login(username, password) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    return request.post('/api/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  /**
   * 注册接口
   * 普通的 JSON 提交
   */
  register(username, password) {
    return request.post('/api/auth/register', {
      username: username,
      password: password
    })
  }
}