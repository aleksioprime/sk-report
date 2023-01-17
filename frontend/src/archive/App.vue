<template>
  <div>
    <!-- <navbar /> -->
    <router-view class="main" />
    <!-- <footbar /> -->
  </div>
  <!-- <div v-else>
    <login-user />
  </div> -->
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from '@/components/BaseNavbar.vue';
import Footbar from '@/components/BaseFootbar.vue';
// import LoginUser from '@/components/UserLogin.vue'
import { mapActions, mapState } from 'vuex'

export default {
  components: {
    Navbar, Footbar
  },
  data() {
    return {
    };
  },
  methods: {
    ...mapActions({
      fetchAuthUser: 'auth/fetchAuthUser'
    }),
  },
  mounted() {
    // this.fetchAuthUser();
  },
  computed: {
    ...mapState({
      auth: state => state.auth.isAuth,
    }),
  },
}
</script>

<style>
@import '@/assets/css/base.css';
.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 220px);
}
</style>
