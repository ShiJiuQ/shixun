const BASE = 'http://127.0.0.1:8000/api/exam'

export const examApi = {

  // 📄 获取试卷
  getPaper: async (year) => {
    const res = await fetch(`${BASE}/paper/${year}`)
    return await res.json()
  },

  // 📚 获取题目列表
  getQuestions: async (params) => {
    const query = new URLSearchParams(params).toString()
    const res = await fetch(`${BASE}/questions?${query}`)
    return await res.json()
  },

  // 🧠 刷题提交（单题）
  submitPractice: async (data) => {
    const res = await fetch(`${BASE}/practice/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return await res.json()
  },

  // 📝 套卷提交
  submitExam: async (data) => {
    const res = await fetch(`${BASE}/exam/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return await res.json()
  }
}