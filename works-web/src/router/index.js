import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },

  // 学生端
  { path: '/student/home',   component: () => import('@/views/StudentHome.vue') },
  { path: '/student/submit', component: () => import('@/views/StudentSubmit.vue') },

  // 教师端
  { path: '/teacher/home',    component: () => import('@/views/TeacherHome.vue') },
  { path: '/teacher/publish', component: () => import('@/views/TeacherPublish.vue') },
  { path: '/teacher/mark',    component: () => import('@/views/TeacherMark.vue') },
  { path: '/teacher/students',component: () => import('@/views/TeacherStudents.vue') },
  { path: '/teacher/manage',  component: () => import('@/views/TeacherManage.vue')},
  {path: '/teacher/manage/:assignment_id', component: () => import('@/views/TeacherManageDetail.vue')}
]

export default createRouter({
  history: createWebHistory(),
  routes
})
