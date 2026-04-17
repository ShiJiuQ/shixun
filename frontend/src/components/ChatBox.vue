<template>
  <el-container class="chat-container">
    <el-header class="chat-header">
      <el-icon><Monitor /></el-icon>
      <span style="margin-left: 10px">研途 Buddy - 408 考研智能助手</span>
    </el-header>

    <el-main class="chat-main">
      <el-scrollbar ref="scrollbarRef">
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

    <el-footer class="chat-footer" height="80px">
      <div class="input-wrapper">
        <el-input
          v-model="userInput"
          placeholder="请输入考研相关问题，按 Enter 发送..."
          @keyup.enter="handleSend"
          :disabled="isLoading"
          clearable
        >
          <template #append>
            <el-button :icon="Promotion" @click="handleSend" :loading="isLoading" type="primary">
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Promotion, User, ChatDotRound, Monitor } from '@element-plus/icons-vue'
import chatApi from '../api/chat'

const userInput = ref('')
const messages = ref([{ role: 'assistant', content: '你好，我是研途 Buddy！准备好开始今天的 408 复习了吗？' }])
const isLoading = ref(false)
const scrollbarRef = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (scrollbarRef.value) {
    // 使用 wrap 获取内部滚动容器
    scrollbarRef.value.setScrollTop(999999)
  }
}

const handleSend = async () => {
  if (!userInput.value.trim() || isLoading.value) return
  
  const text = userInput.value
  messages.value.push({ role: 'user', content: text })
  userInput.value = ''
  isLoading.value = true
  await scrollToBottom()

  const aiMessage = { role: 'assistant', content: '' }
  messages.value.push(aiMessage)

  try {
    await chatApi.streamChat(
      text,
      (chunk) => {
        aiMessage.content += chunk
        scrollToBottom()
      },
      (err) => {
        aiMessage.content = "哎呀，网络开小差了，请确认是否已登录。"
        console.error(err)
      }
    )
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.chat-container { width: 100%; height: 100%; background: white; display: flex; flex-direction: column; }
.chat-header { background: #409eff; color: white; display: flex; align-items: center; font-weight: bold; font-size: 18px; flex-shrink: 0; }
.chat-main { background: #f9fbff; padding: 20px; flex: 1; overflow: hidden; }
.chat-footer { padding: 15px 20px; border-top: 1px solid #ebeef5; flex-shrink: 0; }
.chat-row { display: flex; margin-bottom: 20px; align-items: flex-start; }
.chat-row.user { flex-direction: row-reverse; }
.message-card { max-width: 70%; margin: 0 12px; }
.user .el-card { background-color: #95ec69; border: none; }
.ai-avatar { background: #409eff !important; }
.user-avatar { background: #67c23a !important; }
.content { line-height: 1.6; white-space: pre-wrap; font-size: 14px; }
.input-wrapper { max-width: 100%; }
</style>