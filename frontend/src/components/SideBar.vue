<template>
  <div class="sidebar-container">
    <div class="logo-area">
      <div class="logo-icon">🎓</div>
      <h1 class="logo-text">研途 Buddy</h1>
    </div>

    <el-menu
      :default-active="route.path"
      class="side-menu"
      router
    >
      <el-menu-item index="/chat">
        <el-icon><ChatDotRound /></el-icon>
        <span>AI 智能辅导</span>
      </el-menu-item>
      
      <el-menu-item index="/practice">
        <el-icon><EditPen /></el-icon>
        <span>408 专项刷题</span>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-footer">
      <el-button 
        type="danger" 
        plain 
        class="logout-btn" 
        @click="handleLogout"
      >
        退出登录
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { ChatDotRound, EditPen } from '@element-plus/icons-vue'

const route = useRoute()
const emit = defineEmits(['logout'])

// 向父组件发送退出信号
const handleLogout = () => {
  emit('logout')
}
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #e4e7ed;
}

.logo-area {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f2f5;
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
}

.logo-icon {
  font-size: 30px;
  margin-right: 10px;
}

.logo-text {
  font-size: 20px;
  color: white;
  margin: 0;
  font-weight: bold;
}

.side-menu {
  flex: 1; /* 占据剩余空间 */
  border-right: none;
  padding-top: 15px;
}

/* 菜单激活状态的精致样式 */
.el-menu-item.is-active {
  background-color: #ecf5ff;
  border-right: 3px solid #409eff;
  font-weight: bold;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #f0f2f5;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>