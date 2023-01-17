import { createStore } from 'vuex'
import { authUser } from '@/store/authUser'
import { baseStore } from '@/store/baseStore'

export default createStore({
  
  modules: {
    auth: authUser,
    base: baseStore,
  }
})
