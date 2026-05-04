<template>
  <el-container class="app-container">
    
    <!-- 左侧边栏：会话列表 -->
    <el-aside width="260px" class="sidebar">
      <div class="sidebar-header">
        <el-button type="primary" class="new-chat-btn" @click="handleNewSession">
          <el-icon><Plus /></el-icon> 新建对话
        </el-button>
      </div>
      <el-scrollbar>
        <div class="session-list">
          <div 
            v-for="session in sessionList" 
            :key="session.id"
            :class="['session-item', currentSessionId === session.id ? 'active' : '']"
            @click="switchSession(session.id)"
          >
            <!-- 🌟 注意这里：左边的文字用 session-info 包起来了 -->
            <div class="session-info">
              <el-icon><ChatLineRound /></el-icon>
              <span class="session-title">{{ session.title || '新对话' }}</span>
            </div>
            
            <!-- 🌟 注意这里：这是重命名的图标按钮！ -->
            <el-icon 
              class="edit-btn" 
              @click.stop="handleRenameSession(session)"
            >
              <Edit />
            </el-icon>
          </div>
        </div>
      </el-scrollbar>
    </el-aside>

    <!-- 右侧主体：聊天区域 -->
    <el-container class="chat-container">
      <el-header class="chat-header">
        <el-icon><Monitor /></el-icon>
        <span style="margin-left: 10px">研途 Buddy - 408 考研智能助手</span>
      </el-header>

      <!-- 聊天主区域：支持渲染发送出去的图片 -->
      <el-main class="chat-main">
        <el-scrollbar ref="scrollbarRef">
          <div v-if="messages.length === 0" class="empty-tip">
            请在左侧选择对话，或新建一个对话开始聊天~
          </div>

          <div v-for="(msg, i) in messages" :key="i" :class="['chat-row', msg.role]">
            <el-avatar :size="40" :icon="msg.role === 'user' ? User : ChatDotRound" 
                       :class="msg.role === 'user' ? 'user-avatar' : 'ai-avatar'" />
            <div class="message-card">
              <el-card shadow="hover" :body-style="{ padding: '10px 15px' }">
                
                <!-- 🌟 渲染用户发送的附件缩略图 -->
                <div v-if="msg.files && msg.files.length > 0" class="msg-files">
                  <div v-for="(file, findex) in msg.files" :key="findex" class="msg-file-item">
                    <el-image 
                      v-if="file.isImage" 
                      :src="file.url" 
                      :preview-src-list="[file.url]" 
                      fit="cover" 
                      class="msg-img"
                    />
                    <div v-else class="msg-doc">
                      <el-icon><Document /></el-icon>
                      <span>{{ file.name }}</span>
                    </div>
                  </div>
                </div>

                <div class="content">{{ msg.content }}</div>
              </el-card>
            </div>
          </div>
        </el-scrollbar>
      </el-main>

      <el-footer class="chat-footer">
        <div class="input-wrapper">
          
          <!-- 🌟 新增：文件暂存预览区 (类似 ChatGPT 的小卡片) -->
          <div v-if="stagedFiles.length > 0" class="staging-area">
            <div v-for="(file, index) in stagedFiles" :key="index" class="staged-item">
              <!-- 图片显示缩略图 -->
              <img v-if="file.isImage" :src="file.url" class="staged-img" />
              <!-- 文档显示图标 -->
              <div v-else class="staged-doc-icon"><el-icon><Document /></el-icon></div>
              
              <div class="staged-info">
                <span class="staged-name">{{ file.name }}</span>
              </div>
              
              <!-- 右上角的删除按钮 -->
              <div class="remove-btn" @click="removeStagedFile(index)">
                <el-icon><Close /></el-icon>
              </div>
            </div>
          </div>

          <!-- 隐藏的文件选择器 -->
          <input type="file" ref="fileInputRef" style="display: none" @change="handleFileChange" accept="image/*,.pdf,.doc,.docx" />

          <!-- 输入框本体 -->
          <el-input
            v-model="userInput"
            placeholder="请输入考研相关问题，按 Enter 发送..."
            @keyup.enter="handleSend"
            :disabled="isLoading || !currentSessionId"
            clearable
          >
            <template #prepend>
              <el-button :icon="Paperclip" @click="triggerFileUpload" :disabled="!currentSessionId || isUploading" :loading="isUploading" />
            </template>
            <template #append>
              <el-button :icon="Promotion" @click="handleSend" :loading="isLoading" type="primary" :disabled="!currentSessionId">
                发送
              </el-button>
            </template>
          </el-input>
        </div>
      </el-footer>
    </el-container>

  </el-container>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue'
import { Promotion, User, ChatDotRound, Monitor, Plus, ChatLineRound, Edit, Paperclip, Close, Document } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { chatApi } from '../api/chat'

const mockUserId = 1 

const sessionList = ref([])
const currentSessionId = ref(null)

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const scrollbarRef = ref(null)

const fileInputRef = ref(null) // 获取文件选择器的 DOM
const isUploading = ref(false) // 上传状态 loading

//优化前端界面，希望文件能像现有ai一样在上面，而非一个随便的url
const stagedFiles = ref([])
const triggerFileUpload = () => {
  // 模拟点击隐藏的文件选择器
  fileInputRef.value.click()
}
const scrollToBottom = async () => {
  await nextTick()
  if (scrollbarRef.value) {
    scrollbarRef.value.setScrollTop(99999)
  }
}

const loadSessions = async () => {
  const sessions = await chatApi.getSessions(mockUserId)
  sessionList.value = sessions
  
  if (sessions.length > 0) {
    await switchSession(sessions[0].id)
  } else {
    await handleNewSession()
  }
}

const switchSession = async (sessionId) => {
  if (currentSessionId.value === sessionId) return 
  currentSessionId.value = sessionId
  messages.value = [] 
  
  try {
    const history = await chatApi.getHistory(sessionId)
    if (history && history.length > 0) {
      messages.value = history
    } else {
      messages.value = [{ role: 'assistant', content: '你好，我是研途 Buddy！准备好开始今天的 408 复习了吗？' }]
    }
    await scrollToBottom()
  } catch (error) {
    console.error("加载历史记录失败", error)
  }
}

const handleNewSession = async () => {
  const newSession = await chatApi.createSession(mockUserId)
  if (newSession) {
    sessionList.value.unshift(newSession) 
    await switchSession(newSession.id) 
  }
}

// 🌟 注意这里：处理重命名的核心逻辑
const handleRenameSession = async (session) => {
  try {
    const { value } = await ElMessageBox.prompt('请输入新的对话名称', '重命名', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: session.title === '新对话' ? '' : session.title,
      inputValidator: (val) => {
        if (!val || val.trim() === '') return '对话名称不能为空'
        if (val.length > 20) return '名称不能超过20个字符'
        return true
      }
    })

    const newTitle = value.trim()
    const updatedSession = await chatApi.updateSession(session.id, newTitle)
    
    if (updatedSession) {
      const index = sessionList.value.findIndex(s => s.id === session.id)
      if (index !== -1) {
        sessionList.value[index].title = newTitle
      }
      ElMessage.success('重命名成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('重命名失败')
    }
  }
}

// 🌟 移除暂存区的文件
const removeStagedFile = (index) => {
  stagedFiles.value.splice(index, 1)
}

// 🌟 改造上传方法：上传成功后，塞进暂存区，而不是输入框
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    ElMessage.warning('文件大小不能超过 5MB')
    event.target.value = '' 
    return
  }

  isUploading.value = true
  try {
    const res = await chatApi.uploadFile(file)
    if (res && res.url) {
      ElMessage.success('上传成功！')
      
      // 不再把 Markdown 塞进 userInput，而是存成一个漂亮的对象
      stagedFiles.value.push({
        name: file.name,
        url: res.url,
        isImage: file.type.startsWith('image/')
      })
    }
  } catch (error) {
    ElMessage.error('上传失败，请重试')
  } finally {
    isUploading.value = false
    event.target.value = '' 
  }
}

// 暗中把文字和附件拼接发送
const handleSend = async () => {
  // 如果没打字，也没传文件，就不发送
  if ((!userInput.value.trim() && stagedFiles.value.length === 0) || isLoading.value || !currentSessionId.value) return
  
  // 1. 给页面上显示用的（干净的文本）
  const displayContent = userInput.value.trim()
  // 把暂存区的文件克隆一份存到消息历史里，用来在聊天气泡里渲染缩略图
  const filesToDisplay = [...stagedFiles.value] 
  
  messages.value.push({ 
    role: 'user', 
    content: displayContent, 
    files: filesToDisplay // 挂载文件信息
  })

  // 2. 给后端看的（暗中拼接成 Markdown）
  let backendPayload = userInput.value.trim()
  const markdownAttachments = stagedFiles.value.map(f => 
    f.isImage ? `![${f.name}](${f.url})` : `[${f.name}](${f.url})`
  ).join('\n')

  if (markdownAttachments) {
    backendPayload = backendPayload ? `${backendPayload}\n\n${markdownAttachments}` : markdownAttachments
  }

  // 3. 清理战场
  userInput.value = ''
  stagedFiles.value = [] // 发送完清空暂存区
  isLoading.value = true
  await scrollToBottom()

  // 4. 创建 AI 的回复气泡
  const aiMessage = reactive({ role: 'assistant', content: '' }) 
  messages.value.push(aiMessage)

  try {
    await chatApi.streamChat(
      currentSessionId.value,
      backendPayload, // 🌟 这里发给后端的是带 URL 的暗文
      (chunk) => {
        aiMessage.content += chunk  
        scrollToBottom()
      },
      (err) => {
        aiMessage.content += "\n[网络开小差了，请检查后端]"
        console.error(err)
      }
    )
  } finally {
    isLoading.value = false
  }
}


onMounted(() => {
  loadSessions()
})
</script>

<style scoped>
.app-container {
  height: 100vh;
  width: 100%;
}

.sidebar {
  background-color: #2b2d30;
  display: flex;
  flex-direction: column;
}
.sidebar-header {
  padding: 20px;
}
.new-chat-btn {
  width: 100%;
  border-radius: 8px;
  height: 40px;
}
.session-list {
  padding: 0 10px 20px 10px;
}
.session-item {
  display: flex;
  justify-content: space-between; /* 🌟 保证两端对齐 */
  align-items: center;
  padding: 12px 15px;
  margin-bottom: 8px;
  color: #cfd3dc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.session-item:hover {
  background-color: #3b3e43;
  color: white;
}
.session-item.active {
  background-color: #409eff; 
  color: white;
}
.session-info {
  display: flex;
  align-items: center;
  flex: 1; /* 🌟 抢占空间 */
  overflow: hidden; 
}
.session-title {
  margin-left: 10px;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; 
}

/* 🌟 重命名按钮的样式，我设为了默认显示，绝对不会找不到 */
.edit-btn {
  margin-left: 10px;
  color: #909399; 
  font-size: 16px;
  flex-shrink: 0; /* 🌟 防挤压 */
  transition: all 0.2s;
}
.session-item:hover .edit-btn {
  color: #409eff; 
}
.session-item.active .edit-btn {
  color: white; 
}

/* 🌟 暂存区样式 (输入框上方的区域) */
.chat-footer {
  height: auto !important; /* 让高度自适应暂存区 */
  padding: 15px 20px;
  background: white;
  border-top: 1px solid #ebeef5;
}
.staging-area {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}
.staged-item {
  position: relative;
  width: 80px;
  height: 80px;
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.staged-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}
.staged-doc-icon {
  font-size: 30px;
  color: #909399;
}
.staged-name {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: rgba(0,0,0,0.5);
  color: white;
  font-size: 10px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 2px 0;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}
.remove-btn {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #f56c6c;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.remove-btn:hover { background: #f78989; }

/* 聊天气泡内渲染的文件样式 */
.msg-files {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 8px;
}
.msg-file-item {
  max-width: 200px;
}
.msg-img {
  width: 120px;
  height: 120px;
  border-radius: 6px;
  border: 1px solid #ebeef5;
}
.msg-doc {
  display: flex;
  align-items: center;
  background: #f4f4f5;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  color: #606266;
}
.msg-doc .el-icon { margin-right: 5px; font-size: 16px; }
/* 右侧聊天区样式 */
.chat-container { background: white; display: flex; flex-direction: column; }
.chat-header { background: #409eff; color: white; display: flex; align-items: center; font-weight: bold; font-size: 18px; flex-shrink: 0; }
.chat-main { background: #f9fbff; padding: 20px; flex: 1; overflow: hidden; }
.chat-footer { padding: 15px 20px; border-top: 1px solid #ebeef5; flex-shrink: 0; background: white; }

.empty-tip { text-align: center; color: #909399; margin-top: 100px; font-size: 14px; }
.chat-row { display: flex; margin-bottom: 20px; align-items: flex-start; }
.chat-row.user { flex-direction: row-reverse; }
.message-card { max-width: 70%; margin: 0 12px; }
.user .el-card { background-color: #95ec69; border: none; }
.ai-avatar { background: #409eff !important; }
.user-avatar { background: #67c23a !important; }
.content { line-height: 1.6; white-space: pre-wrap; font-size: 14px; word-break: break-all; }
.input-wrapper { max-width: 100%; }
</style>

