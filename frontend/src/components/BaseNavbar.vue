<template>
  <nav class="navbar navbar-expand-md bg-light">
    <div class="container">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <router-link to="/" class="navbar-brand d-flex align-items-center pe-0">
        <img src="@/assets/img/logo.png" alt="" width="35" class="logo-rotate">
        <span>SKReport</span>
      </router-link>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item dropdown" v-if="checkAdmin">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Администрирование
            </a>
            <ul class="dropdown-menu">
              <router-link to="/user" class="dropdown-item">Пользователи</router-link>
            </ul>
          </li>
          <li class="nav-item">
            <router-link to="/unit" class="nav-link" aria-current="page">Юниты</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/assess" class="nav-link">Оценки</router-link>
          </li>
        </ul>
      </div>
      <span class="navbar-text d-flex align-items-center" v-if="authUser">
        <img :src='authUser.photo ? authUser.photo : require("@/assets/img/user.png")' alt="" width="30" class="me-2">
        <span v-if="authUser.last_name && authUser.first_name">{{ authUser.first_name }} {{ authUser.last_name.slice(0, 1) }}.</span> 
        <span v-else>{{ authUser.username }}</span>
      </span>
      <span class="ms-2">
        <a class="nav-link" href="#" @click="logout">
            Выход
          </a>
      </span>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name:  'BaseNavbar',
  data() {
    return {
    };
  },
  methods: {
    logout() {
      this.$store.dispatch('userLogout').then(() => {
          this.$router.push({ name: 'login' })
        });
    },
  },
  mounted() {
  },
  computed: {
    ...mapGetters(['authUser']),
    // Проверка у текущего пользователя прав администратора
    checkAdmin() {
      if (this.authUser) {
        return this.authUser.role.map(item => item.codename).includes('admin') || this.authUser.is_staff == true
      }
    },
  }
}
</script>

<style>
.pointer {
  cursor: pointer;
}

.logo-rotate {
  display: inline-block;
  margin-right: 10px;
  overflow: hidden;
  -webkit-transition: all 0.5s ease;
  transition: all 0.5s ease;
}

.logo-rotate:hover {
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}
</style>