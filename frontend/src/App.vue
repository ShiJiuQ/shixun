<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" style="background-color: #545c64;">
      <el-menu
        active-text-color="#ffd04b"
        background-color="#545c64"
        text-color="#fff"
        router  
      >
        <el-menu-item index="/">
          <el-icon><ChatDotRound /></el-icon>
          <span>研途 AI 对话</span>
        </el-menu-item>
        <el-menu-item index="/practice">
          <el-icon><Document /></el-icon>
          <span>408 专项刷题</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main style="padding: 0; background-color: #f5f7fa;">
      <router-view></router-view> 
    </el-main>
  </el-container>
</template>

<script setup>
import { ChatDotRound, Document } from '@element-plus/icons-vue'
</script>