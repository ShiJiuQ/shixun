// 如果以后你要写非流式的普通请求（比如获取聊天历史），可以直接用这个 request
import request from '../utils/request' 

// fetch 没法走 axios 拦截器，所以我们需要自己拼一下完整的后端地址
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export const chatApi = {
  /**
   * 流式聊天接口
   * @param {string} message - 用户输入的消息
   * @param {function} onMessage - 收到消息片段时的回调
   * @param {function} onError - 发生错误时的回调
   */
  async streamChat(message, onMessage, onError) {
    const token = localStorage.getItem('token')
    
    try {
      // 🚨 关键修改：告别写死的 127.0.0.1，使用动态 baseURL
      const response = await fetch(`${baseURL}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // fetch 需要手动带 Token
        },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        if (response.status === 401) {
          // 触发后端的门禁机制
          localStorage.removeItem('token')
          window.location.href = '/login'
          throw new Error('登录过期，请重新登录')
        }
        throw new Error(`服务器响应异常: ${response.status}`)
      }

      // 下面全是你队友写的极其优秀的流式解析逻辑，原封不动保留！
      const reader = response.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = '' 

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          if (buffer.trim()) {
            this.processLine(buffer, onMessage)
          }
          break
        }

        buffer += decoder.decode(value, { stream: true })
        let lines = buffer.split('\n')
        buffer = lines.pop() 

        for (const line of lines) {
          this.processLine(line, onMessage)
        }
      }
    } catch (err) {
      console.error('Stream Error:', err)
      onError(err)
    }
  },

  processLine(line, onMessage) {
    const trimmed = line.trim()
    if (!trimmed || trimmed === 'data: [DONE]') return

    if (trimmed.startsWith('data: ')) {
      const content = trimmed.substring(5).trim() 
      if (content) onMessage(content)
    } else {
      onMessage(trimmed)
    }
  }
}