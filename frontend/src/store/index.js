import { createStore } from 'vuex'
import { authUser } from '@/store/authUser'

export default createStore({
  modules: {
    auth: authUser,
  }
})
