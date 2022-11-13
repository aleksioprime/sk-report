<template>
  <navbar/>
  <router-view class="main"/>
  <footbar/>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from '@/components/Navbar.vue';
import Footbar from '@/components/Footbar.vue';

export default {
  components: {
    Navbar, Footbar,
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
