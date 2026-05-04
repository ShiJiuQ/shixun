<!-- src/layout/MainLayout.vue -->
<template>
  <el-container style="height: 100vh;">
    <!-- 左侧导航栏 -->
    <el-aside width="220px" style="background-color: #545c64; display: flex; flex-direction: column;">
      <div class="logo-container">
        <h3 style="color: #fff; text-align: center; padding: 20px 0; margin: 0; border-bottom: 1px solid #666;">
          研途 Buddy
        </h3>
      </div>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#545c64"
        text-color="#fff"
        router
        style="border-right: none;"
        :default-active="$route.path"
      >
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>研途 AI 对话</span>
        </el-menu-item>
        <el-menu-item index="/practice">
          <el-icon><Document /></el-icon>
          <span>408 专项刷题</span>
        </el-menu-item>
        <el-menu-item index="/code-assist">
          <el-icon><Monitor /></el-icon>
          <span>代码辅助平台</span>
        </el-menu-item>
        <el-menu-item index="/study-plan">
          <el-icon><Calendar /></el-icon>
          <span>学习计划模块</span>
        </el-menu-item>
        <el-menu-item index="/emotion">
          <el-icon><Coffee /></el-icon>
          <span>情绪疗愈中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- 右上角 Header -->
      <el-header height="60px" style="background-color: #fff; border-bottom: 1px solid #e4e7ed; display: flex; align-items: center; justify-content: flex-end; padding: 0 20px;">
        <div class="user-profile-entry" @click="$router.push('/profile')" style="cursor: pointer; display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 14px; color: #606266;">个人画像</span>
          <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
        </div>
      </el-header>

      <!-- 业务内容展示区：这里会渲染具体的聊天、刷题等子页面 -->
      <el-main style="padding: 20px; background-color: #f5f7fa;">
        <router-view /> 
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ChatDotRound, Document, Monitor, Calendar, Coffee } from '@element-plus/icons-vue'
</script>

<style scoped>
.logo-container { background-color: #545c64; }
.user-profile-entry:hover { opacity: 0.8; }
.user-profile-entry:hover span { color: #409eff; }
.el-menu { flex: 1; }
</style>