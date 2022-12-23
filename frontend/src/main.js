import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import components from '@/components/UI';
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from '@/store'
import VueCookies from 'vue-cookies';

const app = createApp(App)

components.forEach(component => {
    app.component(component.name, component)
})

app.use(router).use(store).use(VueCookies).use(VueAxios, axios).mount('#app')
