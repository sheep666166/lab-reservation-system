import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/manager/home' },
    {
      path: '/manager',
      name: 'Layout',
      component: () => import('@/layouts/Layout.vue'),
      children: [
        { path: 'home', name: 'Home', component: () => import('@/views/Home.vue') },
        { path: 'lab', name: 'Lab', component: () => import('@/views/Lab.vue') },
        { path: 'profile', name: 'Profile', component: () => import('@/views/Profile.vue') },
        { path: 'password', name: 'password', component: () => import('@/views/Password.vue') },
        { path: 'user', name: 'User', component: () => import('@/views/User.vue') },
        { path: 'equ', name: 'Equ', component: () => import('@/views/Equ.vue') },
        { path: 'lab_equipment', name: 'LabEquipment', component: () => import('@/views/LabEquipment.vue') },
        { path: 'lablist', name: 'LabList', component: () => import('@/views/LabList.vue') },
        { path: 'my-reservation', name: 'MyReservation', component: () => import('@/views/MyReservation.vue') },
        { path: 'audit-reservation', name: 'AuditReservation', component: () => import('@/views/AuditReservation.vue') },
        { path: 'ai-chat', name: 'AIChat', component: () => import('@/views/AIChat.vue') }
      ]
    },
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
    { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') }
  ]
})

import { getToken } from '@/utils/auth'

// 路由守卫：验证token
router.beforeEach((to, from) => {
  const token = getToken()

  if (to.path === '/login' || to.path === '/register') {
    return true
  } else {
    return token ? true : '/login'
  }
})

export default router