import { createStore } from 'vuex'
import { axiosAPI } from '@/axios'
import router from '@/router'

export default createStore({
  state: {
    authUser: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  },
  getters: {
    authUser: state => state.authUser,
    isAuthenticated: state => !!state.accessToken,
    isAdmin: state => (state.authUser && state.authUser.teacher && state.authUser.teacher.admin) || (state.authUser && state.authUser.is_staff),
    isDnevnik: state => (state.authUser && state.authUser.teacher && state.authUser.access_token_dnevnik)
  },
  mutations: {
    setUser(state, user) {
      state.authUser = user;
    },
    clearUser(state) {
      state.authUser = null;
    },
    clearDnevnikToken(state) {
      if (state.authUser && state.authUser.teacher) {
        state.authUser.access_token_dnevnik = null;
      }
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
        localStorage.clear();
      }
    },
    userLogin(context, data) {
      return new Promise((resolve, reject) => {
        axiosAPI.post('token/', {
          username: data.username.toLowerCase(),
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
    },
    async setTokenDnevnik(context, data) {
      function getValueFromHash(hash) {
        return  hash.split('&').reduce(function (res, item) {
          var parts = item.split('=');
          res[parts[0]] = parts[1];
          return res;
        }, {});
      }
      console.log(context);
      if (getValueFromHash(data.route.hash.slice(1)).access_token != context.state.authUser.access_token_dnevnik) {
        console.log('Получен новый токен');
        let updateUser = {
          id: context.state.authUser.id,
          username: context.state.authUser.username,
          first_name: context.state.authUser.first_name,
          last_name: context.state.authUser.last_name,
          email: context.state.authUser.email,
          access_token_dnevnik: getValueFromHash(data.route.hash.slice(1)).access_token,
        }
        await axiosAPI.put(`/user/${updateUser.id}`, updateUser).then((response) => {
          context.commit('setUser', response.data);
          console.log('Пользователь успешно обновлён');
        }).catch((error) => {
          console.log('Ошибка запроса: ', error);
        }).finally(() => {
          router.push(data.route.path)
        })
      } else {
        console.log('Получен старый токен');
        router.push(data.route.path)
      }
    }
  },

  namespaced: true
})