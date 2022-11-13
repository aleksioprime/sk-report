import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import components from '@/components/UI';
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)

components.forEach(component => {
    app.component(component.name, component)
})

app.use(router).use(VueAxios, axios).mount('#app')
