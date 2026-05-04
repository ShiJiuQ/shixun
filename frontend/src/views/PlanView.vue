<template>
  <div class="plan-page">
    <el-row :gutter="20">
      <!-- 日历部分 -->
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>📅 考研倒计时：<b style="color:red">{{ planData.countdown }}</b> 天</template>
          <el-calendar v-model="currentDate">
            <template #date-cell="{ data }">
              <p :class="data.isSelected ? 'is-selected' : ''">
                {{ data.day.split('-').slice(2).join() }}
                {{ getDailyStatus(data.day) }}
              </p>
            </template>
          </el-calendar>
        </el-card>
      </el-col>

      <!-- 任务时间轴 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>📋 今日任务清单</template>
          <el-timeline>
            <el-timeline-item
              v-for="(task, index) in planData.tasks"
              :key="index"
              :type="task.type === 'ai_review' ? 'warning' : 'primary'"
              :hollow="task.done"
              :timestamp="task.type === 'ai_review' ? 'AI 建议复盘' : '自主计划'"
            >
              <el-checkbox v-model="task.done">{{ task.content }}</el-checkbox>
            </el-timeline-item>
          </el-timeline>
          <el-button type="primary" plain style="width:100%">+ 添加个人计划</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const currentDate = ref(new Date())
const planData = ref({ countdown: 0, tasks: [] })

const getDailyStatus = (day) => {
  // 模拟打卡状态：完成标绿，未完成标红
  return day.includes('04') ? '✅' : '' 
}

onMounted(async () => {
  // 假设从 profile 获取压力等级
  const res = await axios.get('http://localhost:8000/api/plan/daily-tasks?stress_level=high')
  planData.value = res.data
})
</script>