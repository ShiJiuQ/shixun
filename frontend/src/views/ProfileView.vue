<template>
  <div class="profile-page">
    <el-row :gutter="20">
      <!-- 用户基本信息 -->
      <el-col :span="8">
        <el-card shadow="hover" class="user-card">
          <el-avatar :size="100" :src="profile.user.avatar" />
          <h2 class="user-name">{{ profile.user.name }}</h2>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="账号">{{ profile.user.account }}</el-descriptions-item>
            <el-descriptions-item label="首选语言">{{ profile.user.language }}</el-descriptions-item>
            <el-descriptions-item label="当前状态">
              <el-tag type="danger">{{ profile.learning_status }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <!-- 🚀 新增：退出登录按钮 -->
          <el-button 
            type="danger" 
            plain 
            style="margin-top: 20px; width: 100%;" 
            @click="handleLogout"
          >
            退出登录
          </el-button>

        </el-card>
      </el-col>

      <!-- 408 能力雷达图（简易版） -->
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>📊 408 各科掌握程度</template>
          <div v-for="item in profile.mastery_radar" :key="item.subject" class="skill-item">
            <span>{{ item.subject }}</span>
            <el-progress :percentage="item.score" :color="customColors" />
          </div>
          <div class="total-stats">
            <el-statistic title="累计刷题总数" :value="profile.total_practice" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router' // 🚀 引入路由用于跳转
// 🚀 替换为带有拦截器的请求工具，解决 401 报错
import request from '../utils/request.js' 

const router = useRouter() // 实例化路由

const profile = ref({
  user: { name: '', avatar: '', account: '', language: '' },
  mastery_radar: [],
  learning_status: '',
  total_practice: 0
})

const customColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

// 🚀 新增：退出登录逻辑
const handleLogout = () => {
  // 1. 清空会话存储中的 Token 和 用户名
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('username')
  
  // 2. 强制跳转到登录页
  router.push('/login')
}

onMounted(async () => {
  try {
    // 🚀 使用 request 发送请求，它会自动把 Token 塞进请求头里
    const res = await request.get('/api/profile/info')
    profile.value = res.data
  } catch (error) {
    console.error('获取画像数据失败:', error)
  }
})
</script>

<style scoped>
.user-card { text-align: center; padding: 20px; }
.user-name { margin: 15px 0; }
.skill-item { margin-bottom: 20px; }
.total-stats { margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }
</style>