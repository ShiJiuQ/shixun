const BASE = 'http://127.0.0.1:8000/api/exam'

export const wrongApi = {

  // ❌ 错题列表
  getWrongList: async (userId) => {
    const res = await fetch(`${BASE}/wrong?user_id=${userId}`)
    return await res.json()
  },

  // 🔁 错题练习
  getWrongPractice: async (userId) => {
    const res = await fetch(`${BASE}/wrong/practice?user_id=${userId}`)
    return await res.json()
  },

  // 提交错题
  submitWrong: async (data) => {
    const res = await fetch(`${BASE}/wrong/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return await res.json()
  }
}