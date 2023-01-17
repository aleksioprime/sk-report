import axios from 'axios'
import cookie from 'vue-cookies'

export const authUser = {
  state: () => ({
    isAuth: false,
    authUser: {},
    authAPI: 'http://localhost:8080/api/v1/auth',
    token: localStorage.getItem('token') || '',
  }),
  getters: {

  },
  mutations: {
    setAuth(state, boolAuth) {
      state.isAuth = boolAuth;
    },
    setUser(state, dataUser) {
      state.authUser = dataUser;
    }
  },
  actions: {
    fetchAuthUser({state, commit}) {
      const config = {
        headers: {
          Authorization: `Bearer ${cookie.get('jwt_token')}`,
        },
      };
      axios.get(state.authAPI, config)
        .then((response) => {
          commit('setAuth', true);
          commit('setUser', response.data);
        })
        .catch((error) => {
          console.log(error);
          commit('setAuth', false);
          commit('setUser', {});
        });
    },
  },
  namespaced: true
}