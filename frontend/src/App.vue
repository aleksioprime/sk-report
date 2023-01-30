<template>
  <div>
    <base-navbar v-if="isAuthenticated" />
    <router-view :class="{ container: isAuthenticated }" class="main"/>
    <base-footbar v-if="isAuthenticated"/>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import BaseNavbar from '@/components/BaseNavbar';
import BaseFootbar from '@/components/BaseFootbar';
import { mapGetters } from 'vuex'

export default {
  components: {
    BaseNavbar, BaseFootbar
  },
  data() {
    return {

    };
  },
  methods: {

  },
  mounted() {
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
}
</script>

<style>
@import '@/assets/css/base.css';
.main {
  /* max-width: 960px; */
  /* margin: 0 auto; */
  /* padding: 20px; */
  min-height: calc(100vh - 220px);
}
</style>
