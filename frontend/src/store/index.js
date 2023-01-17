import { createStore } from 'vuex'
import { axiosAPI } from '@/axios'

export default createStore({
  state: {
    authUser: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  },
  getters: {
    authUser: state => state.authUser,
    isAuthenticated: state => !!state.accessToken
  },
  mutations: {
    setUser(state, user) {
      state.authUser = user;
    },
    clearUser(state, user) {
      state.authUser = null;
    },
    updateToken(state, { access, refresh }) {
      localStorage.setItem('access_token', access);
      state.accessToken = access;
      axiosAPI.defaults.headers.common['Authorization'] = 'Bearer ' + access;
      localStorage.setItem('refresh_token', refresh);
      state.refreshToken = refresh;
      console.log('Токен обновлён')
    },
    destroyToken(state) {
      state.accessToken = null;
      localStorage.removeItem('access_token');
      state.refreshToken = null;
      localStorage.removeItem('refresh_token');
      delete axiosAPI.defaults.headers.common['Authorization'];
    }
  },
  actions: {
    userLogout(context) {
      if (context.getters.isAuthenticated) {
        context.commit('destroyToken');
        context.commit('clearUser');
      }
    },
    userLogin(context, data) {
      return new Promise((resolve, reject) => {
        axiosAPI.post('token/', {
          username: data.username,
          password: data.password
        }).then((response) => {
          context.commit('updateToken', { access: response.data.access, refresh: response.data.refresh });
          console.log('Аутентификация прошла успешно!');
          resolve()
        }).catch((error) => {
          console.log('Ошибка аутентификации');
          context.commit('destroyToken');
          context.commit('clearUser');
          reject(error);
        })
      })
    },
    async getUserData(context) {
      await axiosAPI.get('auth').then((response) => {
        context.commit('setUser', response.data);
        console.log('Данные пользователя успешно получены: ', response.data);
      }).catch((error) => {
        console.log('Ошибка получения данных пользователя: ', error);
      })
    }
  },
  
  namespaced: true
})