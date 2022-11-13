import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '@/views/DashBoard.vue'
import UnitPlans from '@/views/UnitPlans.vue'
import UnitPlansView from '@/views/UnitPlansView.vue'
import UserList from '@/views/UserList.vue'
import Assessment from '@/views/Assessment.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashBoard
  },
  {
    path: '/unitplans',
    name: 'unitplans',
    component: UnitPlans
  },
  {
    path: '/unitplans/:id',
    name: 'unitplansview',
    component: UnitPlansView
  },
  {
    path: '/userlist',
    name: 'userlist',
    component: UserList
  },
  {
    path: '/assessment',
    name: 'assessment',
    component: Assessment
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
