import axios from 'axios'

// Axios 实例用于普通的 JSON 请求（如登录、获取历史记录）
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const chatApi = {
  /**
   * 流式聊天接口
   * @param {string} message - 用户输入的消息
   * @param {function} onMessage - 收到消息片段时的回调 (chunk) => {}
   * @param {function} onError - 发生错误时的回调 (err) => {}
   */
  async streamChat(message, onMessage, onError) {
    const token = localStorage.getItem('token')
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        if (response.status === 401) throw new Error('登录过期，请重新登录')
        throw new Error(`服务器响应异常: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = '' 

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          // 【关键修改 1】流结束时，如果 buffer 里还有没凑够一行的数据，强制处理掉
          if (buffer.trim()) {
            this.processLine(buffer, onMessage)
          }
          break
        }

        // 解码当前接收到的字节块
        buffer += decoder.decode(value, { stream: true })

        // 【关键修改 2】按单换行符分割，保证实时性
        // SSE 规范虽然是双换行符结束一段，但数据通常按行传输
        let lines = buffer.split('\n')
        
        // 最后一个元素如果不是以换行符结尾，说明是不完整的，存入 buffer 等下一轮
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

  /**
   * 处理每一行 SSE 数据
   */
  processLine(line, onMessage) {
    const trimmed = line.trim()
    
    // 忽略空行、注释或结束标志
    if (!trimmed || trimmed === 'data: [DONE]') {
      return
    }

    // 严格解析以 "data: " 开头的行
    if (trimmed.startsWith('data: ')) {
      // 提取 data: 之后的内容（支持内容中本身包含空格）
      const content = trimmed.substring(5).trim() 
      if (content) {
        onMessage(content)
      }
    } else {
      // 兜底逻辑：如果后端发来的行没带 data: 前缀，也尝试作为内容发送
      // 这能解决部分因后端格式不标准导致的憋字
      onMessage(trimmed)
    }
  }
}

export default chatApi