import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
   {
    path: '/',
    component: HomeView
  },
  {
    path: '/login',
    component: LoginView
  },
   {
    path: '/register',
    component: SignupView   
  },
  {
  path: '/lecture/:id',
  name: 'LectureDetail',
  component: () => import('../views/LectureDetailView.vue') 
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router