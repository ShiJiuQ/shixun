// frontend/src/api/chat.js

export const chatApi = {
  // 1. 获取当前用户的所有会话列表 (🌟 新增)
  getSessions: async (userId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/chat/sessions?user_id=${userId}`)
      if (!response.ok) throw new Error('获取会话列表失败')
      return await response.json()
    } catch (error) {
      console.error(error)
      return []
    }
  },

  // 2. 创建一个新会话 (🌟 新增)
  createSession: async (userId) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      })
      if (!response.ok) throw new Error('创建会话失败')
      return await response.json()
    } catch (error) {
      console.error(error)
      return null
    }
  },
  updateSession: async (sessionId, title) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/chat/sessions/${sessionId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: title // 这里传我们新起的名字
        })
      })
      if (!response.ok) throw new Error('修改会话失败')
      return await response.json()
    } catch (error) {
      console.error(error)
      return null
    }
  },
  // 3. 获取会话的历史记录 (保持你原来的)
  getHistory: async (sessionId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/chat/sessions/${sessionId}/messages`)
      if (!response.ok) throw new Error('获取历史记录失败')
      return await response.json()
    } catch (error) {
      console.error(error)
      return []
    }
  },

  uploadFile: async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file) 

      const response = await fetch('http://127.0.0.1:8000/api/chat/upload', {
        method: 'POST',
        body: formData // 用 FormData 上传，浏览器会自动处理 headers
      })
      
      if (!response.ok) throw new Error('文件上传失败')
      return await response.json() 
    } catch (error) {
      console.error(error)
      return null
    }
  },
  
  // 4. 发送流式对话请求 (保持你原来的)
  streamChat: async (sessionId, text, onChunk, onError) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          content: text,
          role: 'user',
          message_type: 'text'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 解析 SSE 流
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n\n');
        
        for (let line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              return; // 结束推流
            } else if (data.startsWith('[ERROR]')) {
              if (onError) onError(new Error(data));
              return;
            } else {
              // 把每一个字传给 Vue 的回调函数去渲染
              if (onChunk) onChunk(data);
            }
          }
        }
      }
    } catch (error) {
      if (onError) onError(error);
    }
  }
}