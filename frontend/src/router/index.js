import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MainLayout from '../layout/MainLayout.vue' // 确保你创建了这个布局文件

const router = createRouter({
  // 使用 Vite 环境变量，更加严谨
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView // 登录页独立，不嵌套在 MainLayout 中
    },
    {
      path: '/',
      component: MainLayout, 
      redirect: '/chat',
      children: [
        {
          path: 'chat',
          name: 'chat',
          component: () => import('../views/ChatView.vue')
        },
        {
          path: 'practice',
          name: 'practice',
          component: () => import('../views/PracticeView.vue')
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileView.vue')
        },
        {
          path: 'study-plan',
          name: 'study-plan',
          component: () => import('../views/PlanView.vue')
        },
        {
          path: 'emotion',
          name: 'emotion',
          component: () => import('../views/EmotionView.vue')
        }
      ]
    }
  ]
})

// 路由守卫逻辑
router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('token'); 
  const isValidToken = token && token !== 'undefined' && token !== 'null' && token !== '';

  if (to.name !== 'login' && !isValidToken) {
    next({ name: 'login' });
  } 
  else if (to.name === 'login' && isValidToken) {
    next({ name: 'chat' });
  } 
  else {
    next(); 
  }
});

// 把组装好的 router 交给 main.js！
export default router;