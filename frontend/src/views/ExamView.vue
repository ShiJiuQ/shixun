<template>
  <div class="exam-container">

    <!-- 🔥 模式切换 -->
    <el-radio-group v-model="mode" @change="init">
      <el-radio-button label="practice">练习模式</el-radio-button>
      <el-radio-button label="exam">套卷模式</el-radio-button>
      <el-radio-button label="wrong">错题重练</el-radio-button>
    </el-radio-group>

    <!-- ⏱️ 套卷计时 -->
    <div v-if="mode === 'exam'" class="timer">
      剩余时间：{{ timeLeft }} 秒
    </div>

    <el-row style="margin-top: 20px">

      <!-- 📄 题号导航（套卷模式） -->
      <el-col :span="4" v-if="mode === 'exam'">
        <el-menu>
          <el-menu-item
            v-for="(q,i) in questions"
            :key="q.question_id"
            @click="currentIndex=i"
          >
            {{ i + 1 }}
          </el-menu-item>
        </el-menu>
      </el-col>

      <!-- 📚 题目 -->
      <el-col :span="14">
        <el-card v-if="currentQuestion">
          <h3>{{ currentQuestion.question_content }}</h3>

          <el-radio-group v-model="answers[currentQuestion.question_id]">
            <el-radio
              v-for="(v,k) in currentQuestion.options"
              :key="k"
              :label="k"
            >
              {{ k }}. {{ v }}
            </el-radio>
          </el-radio-group>
        </el-card>
      </el-col>

      <!-- 👉 操作区 -->
      <el-col :span="6">
        <el-button type="primary" @click="submit">
          提交
        </el-button>

        <div v-if="result" style="margin-top: 20px">
          <p v-if="mode === 'exam'">总分：{{ result.total_score }}</p>
          <p v-else>结果：{{ result.is_correct ? '正确' : '错误' }}</p>
        </div>
      </el-col>

    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { examApi } from '../api/exam'
import { wrongApi } from '../api/wrong'

const route = useRoute()

const mode = ref('practice')
const questions = ref([])
const currentIndex = ref(0)
const answers = ref({})
const result = ref(null)

const timeLeft = ref(0)
let timer = null
const sessionId = ref(null)

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value]
})

// 🚀 初始化
const init = async () => {
  result.value = null
  answers.value = {}

  if (mode.value === 'practice') {
    const res = await examApi.getQuestions({ page: 1, page_size: 5 })
    questions.value = res.data.list
  }

  else if (mode.value === 'exam') {
    const res = await examApi.getPaper(2020)
    questions.value = res.data

    // 启动 session
    const s = await fetch('http://127.0.0.1:8000/api/exam/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: "1", paper_id: "2020" })
    })
    const data = await s.json()

    sessionId.value = data.data.session_id
    timeLeft.value = data.data.duration * 60

    startTimer()
  }

  else if (mode.value === 'wrong') {
    const res = await wrongApi.getWrongPractice("1")
    questions.value = res.data
  }

  currentIndex.value = 0
}

// ⏱️ 倒计时
const startTimer = () => {
  clearInterval(timer)

  timer = setInterval(() => {
    timeLeft.value--

    if (timeLeft.value <= 0) {
      clearInterval(timer)
      submit()
    }
  }, 1000)
}

// 📤 提交
const submit = async () => {
  const payload = Object.keys(answers.value).map(k => ({
    question_id: k,
    answer: answers.value[k]
  }))

  if (mode.value === 'practice') {
    const res = await examApi.submitPractice({
      user_id: "1",
      question_id: payload[0].question_id,
      answer: payload[0].answer
    })
    result.value = res.data
  }

  else if (mode.value === 'exam') {
    const res = await fetch('http://127.0.0.1:8000/api/exam/submit_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        user_id: "1",
        answers: payload
      })
    })
    const data = await res.json()
    result.value = data.data
  }

  else if (mode.value === 'wrong') {
    const res = await wrongApi.submitWrong({
      user_id: "1",
      answers: payload
    })
    result.value = res.data[0]
  }
}

// 初始化
onMounted(() => {
  if (route.query.mode) {
    mode.value = route.query.mode
  }
  init()
})
</script>

<style scoped>
.exam-container {
  padding: 20px;
}
.timer {
  color: red;
  font-size: 18px;
  margin-top: 10px;
}
</style>