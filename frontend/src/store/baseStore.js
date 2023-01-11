import cookie from 'vue-cookies'

export const baseStore = {
  state: () => ({
    baseAPI: 'http://localhost:8080/api/v1',
    configJWT: {
      headers: {
        Authorization: `Bearer ${cookie.get('jwt_token')}`,
      },
    },
  }),
  getters: {

  },
  mutations: {
    
  },
  actions: {
    
  },
  namespaced: true
}