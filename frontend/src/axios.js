import axios from 'axios'

const axiosAPI = axios.create({
  baseURL: 'http://localhost:8080/api/v1/',
})

axiosAPI.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');

axiosAPI.interceptors.response.use(resp => resp, async error => {
  const originalConfig = error.config;
  if (originalConfig.url != "/login" && error.response) {
    if (error.response.status == 401 && !originalConfig._retry) {
      console.log('Ошибка авториации. Возможно, токен устрарел');
      originalConfig._retry = true;
      const rs = await axiosAPI.post('token/refresh/', {
        "refresh": localStorage.getItem('refresh_token'),
      });
      console.log('Обновлённый токен успешно получен');
      localStorage.setItem('access_token', rs.data.access);
      originalConfig.headers = {
        ...originalConfig.headers,
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      }
      return axiosAPI(originalConfig)
    }
  }
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  return Promise.reject(error);
})

export { axiosAPI }