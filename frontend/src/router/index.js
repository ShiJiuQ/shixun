import { createRouter, createWebHistory } from 'vue-router'
// 引入你的页面组件
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  // import.meta.env.BASE_URL 是 Vite 的标准写法，比留空更严谨
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',          
      redirect: '/login'  // 默认打开根目录时，自动跳转到登录页
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView // 登录页组件
    },
    {
      path: '/chat',
      name: 'chat',
      // 大厂习惯：聊天页使用“懒加载”（箭头函数 import），只有用户真正进去了才下载这个页面的代码，提升速度
      component: () => import('../views/ChatView.vue') 
    }
    // 以后队友写了新页面，比如 practice，就在这里加一段：
    // { path: '/practice', name: 'practice', component: () => import('../views/PracticeView.vue') }
  ]
})

// 🚀 全局前置路由守卫（前端的“铁面保安”）
router.beforeEach((to, from, next) => {
  // 1. 去浏览器的本地保险箱里找一找有没有 token
  const token = localStorage.getItem('token')

  // 2. 判断逻辑：如果用户想去的页面不是登录页，并且他手里没有 token
  if (to.name !== 'login' && !token) {
    // 强制把他送回登录页
    next({ name: 'login' })
  } else {
    // 其他情况（比如去登录页，或者有 token 去聊天页），正常放行
    next()
  }
})

export default router