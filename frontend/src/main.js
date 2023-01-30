import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import components from '@/components/UI';
import { axiosAPI }  from './axios.js'
import store from '@/store'
import VueCookies from 'vue3-cookies';

router.beforeEach(async (to) => {
  const user = store.getters['authUser'];
  const token = localStorage.getItem('access_token');
  if (to.name !== 'unitmypview') {
    localStorage.removeItem('currentTab');
  }
  if (!token && to.name !== 'login') {
    console.log('Не найден токен в localStorage: выполняется разлогирование');
    await store.dispatch('userLogout');
    return { name: 'login' }
  }
  if (!user && token) {
    console.log('Найден токен в localStorage: запрос данных пользователя');
    await store.dispatch('getUserData').then(() => {
      return { name: to.name }
    });
  }
  if (to.name == 'login' && token) {
    console.log('Вы залогинены: перенаправление на главную страницу');
    return { name: 'unitlist' }
  }
})

const app = createApp(App)
app.config.globalProperties.axios=axiosAPI

components.forEach(component => {
  app.component(component.name, component)
})

app.use(router).use(store).use(VueCookies).mount('#app')
