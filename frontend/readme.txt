1. Установить Node.js и npm
2. Установить vue-cli
npm install -g @vue/cli
3. Создание проекта 
vue create frontend
4. Запуск сервера
npm run serve

Установить пакет для csrf
npm install vue-cookies
Установить пакет для bootstrap
npm install --save @popperjs/core
npm install --save bootstrap
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
Установить пакет для coockies
npm install vue3-cookies --save
import { useCookies } from "vue3-cookies";
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },

Установить axios
npm install --save axios vue-axios
import axios from 'axios'
import VueAxios from 'vue-axios'
const app = Vue.createApp(...)
app.use(VueAxios, axios)