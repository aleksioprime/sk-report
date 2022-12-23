<template>
  <div v-if="$store.state.auth.isAuth">
    <navbar />
    <router-view class="main" />
    <footbar />
  </div>
  <div v-else>
    <login-user />
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from '@/components/Navbar.vue';
import Footbar from '@/components/Footbar.vue';
import LoginUser from '@/components/LoginUser.vue'
import { mapActions } from 'vuex'

export default {
  components: {
    Navbar, Footbar, LoginUser
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
    this.fetchAuthUser();
  }
}
</script>

<style>
.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 220px);
}
</style>
