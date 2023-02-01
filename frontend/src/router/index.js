import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '@/views/UserLogin.vue'
import DashBoard from '@/views/DashBoard.vue'
import UnitList from '@/views/UnitList.vue'
import UnitMYPView from '@/views/UnitMYPView.vue'
import UserList from '@/views/UserList.vue'
import AssessList from '@/views/AssessList.vue'


const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: UnitList,
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/unit',
    name: 'unitlist',
    component: UnitList,
  },
  {
    path: '/unit/:id',
    name: 'unitmypview',
    component: UnitMYPView,
  },
  {
    path: '/user',
    name: 'userlist',
    component: UserList
  },
  {
    path: '/assess',
    name: 'assesslist',
    component: AssessList,
  },
]

const router = createRouter({
  routes,
  history: createWebHistory(),
})

export default router
