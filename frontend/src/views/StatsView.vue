<template>
  <div>
    <el-card>
      <h2>学习统计</h2>

      <p>总做题数：{{ stats.total }}</p>
      <p>正确率：{{ stats.accuracy }}%</p>

      <el-progress :percentage="stats.accuracy" />

    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({
  total: 0,
  accuracy: 0
})

onMounted(async () => {
  const res = await fetch('http://127.0.0.1:8000/api/exam/stats?user_id=1')
  const data = await res.json()
  stats.value = data.data
})
</script>