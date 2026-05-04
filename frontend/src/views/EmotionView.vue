<template>
  <div class="emotion-page" style="text-align: center;">
    <el-card>
      <!-- 小精灵动画占位[cite: 2] -->
      <div class="sprite-container">
        <div class="sprite-icon">🧚</div>
        <p class="suggestion-bubble">{{ emotionData.suggestion }}</p>
      </div>

      <el-divider>选择你当前的状态标签</el-divider>
      <el-check-tag
        v-for="tag in availableTags"
        :key="tag"
        :checked="selectedTags.includes(tag)"
        @change="toggleTag(tag)"
        style="margin: 5px"
      >
        {{ tag }}
      </el-check-tag>

      <div style="margin-top: 30px">
        <el-input
          v-model="chatInput"
          placeholder="有什么压力想对小精灵说说吗？"
          @keyup.enter="analyzeMood"
        >
          <template #append>
            <el-button @click="analyzeMood">倾诉</el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emotionData = ref({ suggestion: '你好！我是你的研途精灵，今天感觉怎么样？' })
const chatInput = ref('')
const availableTags = ['焦虑', '想喝奶茶', '计组太难了', '斗志昂扬', '想睡觉']
const selectedTags = ref([])

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) selectedTags.value.splice(index, 1)
  else selectedTags.value.push(tag)
}

const analyzeMood = async () => {
  const res = await axios.post(`http://localhost:8000/api/emotion/analyze?text=${chatInput.value}`)
  emotionData.value = res.data
  chatInput.value = ''
}
</script>

<style scoped>
.sprite-icon { font-size: 80px; animation: float 3s infinite ease-in-out; }
.suggestion-bubble {
  background: #fdf6ec;
  padding: 15px;
  border-radius: 15px;
  display: inline-block;
  margin: 20px 0;
  border: 1px solid #faecd8;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
</style>