import axios from 'axios'
import store from '@/store'
import cookie from 'vue3-cookies'

const axiosAPI = axios.create({
  baseURL: '/api/v1/',
})

axiosAPI.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');

axiosAPI.interceptors.response.use(resp => resp, async error => {
  const originalConfig = error.config;
  if (originalConfig.url != "/login" && error.response) {
    if (error.response.status == 401 && error.response.data.code == 'user_not_found') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.reload();
    }
    if (error.response.status == 401 && !originalConfig._retry) {
      // console.log('Ошибка авториации. Возможно, токен устрарел');
      originalConfig._retry = true;
      // Запрос нового токена access по текущему токену refresh
      const rs = await axiosAPI.post('token/refresh/', {
        "refresh": localStorage.getItem('refresh_token'),
      });
      // console.log('Обновлённый токен успешно получен');
      localStorage.setItem('access_token', rs.data.access);
      // Обновление токена для текущего запроса
      originalConfig.headers = {
        ...originalConfig.headers,
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      }
      // Обновление токена для будущих запросов
      axiosAPI.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');
      return axiosAPI(originalConfig)
    }
  }
  return Promise.reject(error);
})

export { axiosAPI }