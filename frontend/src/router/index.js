import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '@/views/UserLogin.vue'
import DashBoard from '@/views/DashBoard.vue'

import AdminEmployee from '@/views/AdminEmployee.vue'
import AdminStudent from '@/views/AdminStudent.vue'
import AdminGroup from '@/views/AdminGroup.vue'
import AdminSubject from '@/views/AdminSubject.vue'
import AdminWorkLoad from '@/views/AdminWorkLoad.vue'
import AdminSyllabus from '@/views/AdminSyllabus.vue'
import UnitMYP from '@/views/UnitMYP.vue'
import UnitMYPView from '@/views/UnitMYPView.vue'
import UnitMYPIDView from '@/views/UnitMYPIDView.vue'
import UnitDP from '@/views/UnitDP.vue'
import UnitDPView from '@/views/UnitDPView.vue'
import ReportTeacher from '@/views/ReportTeacher.vue'
import ReportPsychologist from '@/views/ReportPsychologist.vue' 
import ReportMentor from '@/views/ReportMentor.vue'
import AssessSchedule from '@/views/AssessSchedule.vue'
import AssessList from '@/views/AssessList.vue'
import AssessWorkView from '@/views/AssessWorkView.vue'
import AssessPeriodView from '@/views/AssessPeriodView.vue'
import ExtraContest from '@/views/ExtraContest.vue'
import ExtraTeaching from '@/views/ExtraTeaching.vue'
import AssessReportTeacher from '@/views/AssessReportTeacher.vue'
import AssessReportPsychologist from '@/views/AssessReportPsychologist.vue'
import AssessReportMentor from '@/views/AssessReportMentor.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashBoard,
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/myp',
    name: 'unitmyp',
    component: UnitMYP,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/myp/:id',
    name: 'unitmypview',
    component: UnitMYPView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/myp/idu/:id',
    name: 'unitmypidview',
    component: UnitMYPIDView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/dp',
    name: 'unitdp',
    component: UnitDP,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/dp/:id',
    name: 'unitdpview',
    component: UnitDPView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/student',
    name: 'student',
    component: AdminStudent
  },
  {
    path: '/employee',
    name: 'employee',
    component: AdminEmployee
  },
  {
    path: '/group',
    name: 'group',
    component: AdminGroup
  },
  {
    path: '/workload',
    name: 'workload',
    component: AdminWorkLoad
  },
  {
    path: '/syllabus',
    name: 'syllabus',
    component: AdminSyllabus
  },
  {
    path: '/subject',
    name: 'subject',
    component: AdminSubject
  },
  {
    path: '/assessment',
    name: 'assesslist',
    component: AssessList,
  },
  {
    path: '/report/teacher',
    name: 'assessReportTeacher',
    component: AssessReportTeacher,
  },
  {
    path: '/report/psychologist',
    name: 'assessReportPsychologist',
    component: AssessReportPsychologist,
  },
  {
    path: '/report/mentor',
    name: 'assessReportMentor',
    component: AssessReportMentor,
  },
  {
    path: '/schedule',
    name: 'assessSchedule',
    component: AssessSchedule,
  },
  {
    path: '/assessment/sumwork/:id',
    name: 'assessworkview',
    component: AssessWorkView,
  },
  {
    path: '/assessment/group/:id_group/period/:id_period/subject/:id_subject',
    name: 'assessPeriodView',
    component: AssessPeriodView,
  },
  {
    path: '/report/teacher/group/:id_group/period/:id_period/subject/:id_subject/author/:id_author',
    name: 'reportTeacherId',
    component: ReportTeacher,
  },
  {
    path: '/report/teacher/group/:id_group/period/:id_period/subject/:id_subject',
    name: 'reportTeacherAll',
    component: ReportTeacher,
  },
  {
    path: '/report/psychologist/group/:id_group/period/:id_period',
    name: 'reportPsychologist',
    component: ReportPsychologist,
  },
  {
    path: '/report/mentor/group/:id_group/period/:id_period',
    name: 'reportMentor',
    component: ReportMentor,
  },
  {
    path: '/extra/contest',
    name: 'extraContest',
    component: ExtraContest,
  },
  {
    path: '/extra/teaching',
    name: 'extraTeaching',
    component: ExtraTeaching,
  },
]

const router = createRouter({
  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return { top: 0 }
  },
  routes,
  history: createWebHistory(),
})

export default router
