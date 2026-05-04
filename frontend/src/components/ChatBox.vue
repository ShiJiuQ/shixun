<template>
  <el-container class="app-container">
    
    <!-- ==================== 左侧边栏：会话列表 ==================== -->
    <el-aside width="260px" class="sidebar">
      <!-- 新建对话按钮 -->
      <div class="sidebar-header">
        <el-button type="primary" class="new-chat-btn" @click="handleNewSession">
          <el-icon><Plus /></el-icon> 新建对话
        </el-button>
      </div>
      
      <!-- 会话列表滚动区 -->
      <el-scrollbar>
        <div class="session-list">
          <div 
            v-for="session in sessionList" 
            :key="session.id"
            :class="['session-item', currentSessionId === session.id ? 'active' : '']"
            @click="switchSession(session.id)"
          >
            <!-- 左边的图标和文字包在一起 -->
            <div class="session-info">
              <el-icon><ChatLineRound /></el-icon>
              <span class="session-title">{{ session.title || '新对话' }}</span>
            </div>
            
            <!-- 🌟 右边的编辑重命名按钮 (使用原生 Emoji，绝对不会不显示) -->
            <div 
              class="edit-btn" 
              @click.stop="handleRenameSession(session)"
              title="重命名对话"
            >
              ✏️
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-aside>

    <!-- ==================== 右侧主体：聊天区域 ==================== -->
    <el-container class="chat-container">
      <!-- 顶部标题 -->
      <el-header class="chat-header">
        <el-icon><Monitor /></el-icon>
        <span style="margin-left: 10px">研途 Buddy - 408 考研智能助手</span>
      </el-header>

      <!-- 聊天内容区 -->
      <el-main class="chat-main">
        <el-scrollbar ref="scrollbarRef">
          <!-- 消息为空时的占位提示 -->
          <div v-if="messages.length === 0" class="empty-tip">
            请在左侧选择对话，或新建一个对话开始聊天~
          </div>

          <!-- 聊天气泡循环渲染 -->
          <div v-for="(msg, i) in messages" :key="i" :class="['chat-row', msg.role]">
            <el-avatar :size="40" :icon="msg.role === 'user' ? User : ChatDotRound" 
                       :class="msg.role === 'user' ? 'user-avatar' : 'ai-avatar'" />
            <div class="message-card">
              <el-card shadow="hover" :body-style="{ padding: '10px 15px' }">
                <div class="content">{{ msg.content }}</div>
              </el-card>
            </div>
          </div>
        </el-scrollbar>
      </el-main>

      <!-- 底部输入框区 -->
      <el-footer class="chat-footer" height="80px">
        <div class="input-wrapper">
          <el-input
            v-model="userInput"
            placeholder="请输入考研相关问题，按 Enter 发送..."
            @keyup.enter="handleSend"
            :disabled="isLoading || !currentSessionId"
            clearable
          >
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
import { Promotion, User, ChatDotRound, Monitor, Plus, ChatLineRound } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { chatApi } from '../api/chat'

const mockUserId = 1 // 模拟当前登录的用户ID

const sessionList = ref([])
const currentSessionId = ref(null)

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const scrollbarRef = ref(null)

// --- 滚动到底部 ---
const scrollToBottom = async () => {
  await nextTick()
  if (scrollbarRef.value) {
    scrollbarRef.value.setScrollTop(99999)
  }
}

// --- 初始化加载：查会话列表 ---
const loadSessions = async () => {
  const sessions = await chatApi.getSessions(mockUserId)
  sessionList.value = sessions
  
  if (sessions.length > 0) {
    await switchSession(sessions[0].id)
  } else {
    await handleNewSession()
  }
}

// --- 切换会话 ---
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

// --- 新建会话 ---
const handleNewSession = async () => {
  const newSession = await chatApi.createSession(mockUserId)
  if (newSession) {
    sessionList.value.unshift(newSession) 
    await switchSession(newSession.id) 
  }
}

// --- 🌟 重命名会话 (核心逻辑) ---
const handleRenameSession = async (session) => {
  try {
    // 1. 弹出输入框
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

    // 2. 调后端接口改名
    const newTitle = value.trim()
    const updatedSession = await chatApi.updateSession(session.id, newTitle)
    
    if (updatedSession) {
      // 3. 改名成功，瞬间刷新左侧列表
      const index = sessionList.value.findIndex(s => s.id === session.id)
      if (index !== -1) {
        sessionList.value[index].title = newTitle
      }
      ElMessage.success('重命名成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重命名报错:', error)
      ElMessage.error('重命名失败，请检查后端报错')
    }
  }
}

// --- 发送消息 ---
const handleSend = async () => {
  if (!userInput.value.trim() || isLoading.value || !currentSessionId.value) return
  
  const text = userInput.value
  messages.value.push({ role: 'user', content: text })
  userInput.value = ''
  isLoading.value = true
  await scrollToBottom()

  const aiMessage = reactive({ role: 'assistant', content: '' }) 
  messages.value.push(aiMessage)

  try {
    await chatApi.streamChat(
      currentSessionId.value,
      text,
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
/* ==========================================
   1. 全局布局：左右分栏，占满全屏
   ========================================== */
.app-container {
  height: 100vh;
  width: 100%;
  display: flex; 
}

/* ==========================================
   2. 左侧边栏样式 (深色极客风)
   ========================================== */
.sidebar {
  background-color: #2b2d30;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #1e1f22;
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
  justify-content: space-between; 
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

/* 🌟 核心防挤压装甲：给文字区域 flex: 1 抢占空间，超出的文字变省略号 */
.session-info {
  display: flex;
  align-items: center;
  flex: 1; 
  overflow: hidden; 
}
.session-title {
  margin-left: 10px;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; 
}

/* 🌟 核心防挤压装甲：右侧按钮不允许被压缩 (flex-shrink: 0) */
.edit-btn {
  margin-left: 10px;
  color: #909399; 
  font-size: 14px; 
  transition: all 0.2s;
  flex-shrink: 0; 
}
.session-item:hover .edit-btn {
  transform: scale(1.1); /* 鼠标滑过时稍微放大一点点，提升手感 */
}

/* ==========================================
   3. 右侧聊天区样式
   ========================================== */
.chat-container { 
  background: white; 
  display: flex; 
  flex-direction: column; 
  flex: 1; 
}
.chat-header { 
  background: #409eff; 
  color: white; 
  display: flex; 
  align-items: center; 
  font-weight: bold; 
  font-size: 18px; 
  flex-shrink: 0; 
}
.chat-main { 
  background: #f9fbff; 
  padding: 20px; 
  flex: 1; 
  overflow: hidden; 
}
.chat-footer { 
  padding: 15px 20px; 
  border-top: 1px solid #ebeef5; 
  flex-shrink: 0; 
  background: white; 
}
.empty-tip { 
  text-align: center; 
  color: #909399; 
  margin-top: 100px; 
  font-size: 14px; 
}
.chat-row { 
  display: flex; 
  margin-bottom: 20px; 
  align-items: flex-start; 
}
.chat-row.user { 
  flex-direction: row-reverse; 
}
.message-card { 
  max-width: 70%; 
  margin: 0 12px; 
}
.user .el-card { 
  background-color: #95ec69; 
  border: none; 
}
.ai-avatar { background: #409eff !important; }
.user-avatar { background: #67c23a !important; }
.content { 
  line-height: 1.6; 
  white-space: pre-wrap; 
  font-size: 14px; 
  word-break: break-all; 
}
.input-wrapper { 
  max-width: 100%; 
}
</style>