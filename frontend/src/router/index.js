import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '@/views/DashBoard.vue'
import UnitList from '@/views/UnitList.vue'
import UnitView from '@/views/UnitView.vue'
// import UserList from '@/views/UserList.vue'
import AssessList from '@/views/AssessList.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashBoard
  },
  {
    path: '/unit',
    name: 'unitlist',
    component: UnitList
  },
  {
    path: '/unit/:id',
    name: 'unitview',
    component: UnitView
  },
  // {
  //   path: '/user',
  //   name: 'userlist',
  //   component: UserList
  // },
  {
    path: '/assess',
    name: 'assesslist',
    component: AssessList
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
