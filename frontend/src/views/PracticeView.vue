<template>
  <div class="practice-page">
    <el-card v-if="currentQuestion">
      <template #header>
        <el-tag>{{ currentQuestion.subject }}</el-tag>
        <span style="margin-left:10px">{{ currentQuestion.content }}</span>
      </template>
      <el-radio-group v-model="selectedOption" class="options-group">
        <el-radio v-for="opt in currentQuestion.options" :key="opt" :label="opt">{{ opt }}</el-radio>
      </el-radio-group>
    </el-card>

    <el-card style="margin-top:20px">
      <template #header>💻 算法代码分析 (408 专项)</template>
      <el-input
        v-model="codeSnippet"
        type="textarea"
        :rows="8"
        placeholder="在这里输入你的算法代码，例如链表删除逻辑..."
      />
      <el-button type="success" @click="submitCode" style="margin-top:10px">AI 诊断代码</el-button>
      
      <div v-if="diagResult" class="diag-res">
        <el-alert :title="diagResult.message" :type="diagResult.status === 'error' ? 'error' : 'success'" show-icon />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const currentQuestion = ref(null)
const selectedOption = ref('')
const codeSnippet = ref('')
const diagResult = ref(null)

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/practice/get-question')
  currentQuestion.value = res.data
})

const submitCode = async () => {
  const res = await axios.post('http://localhost:8000/api/practice/submit-code', { code: codeSnippet.value })
  diagResult.value = res.data
}
</script>