import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import components from '@/components/UI';
import { axiosAPI }  from './axios.js'
import store from '@/store'

router.beforeEach(async (to, from, next) => {
  const user = store.getters['getUser'];
  const token = localStorage.getItem('access_token');
  if (!token && to.name !== 'login') {
    console.log('Не найден токен в localStorage: выполняется разлогирование');
    await store.dispatch('userLogout');
    next('login');
  }
  if (!user && token) {
    console.log('Найден токен в localStorage: запрос данных пользователя');
    await store.dispatch('getUserData');
  }
  if (to.name == 'login' && token) {
    console.log('Вы залогинены: перенаправление на главную страницу');
    next('dashboard');
  }
  next();
})

const app = createApp(App)
app.config.globalProperties.axios=axiosAPI

components.forEach(component => {
  app.component(component.name, component)
})

app.use(router).use(store).mount('#app')
