<template>
  <nav class="navbar navbar-expand-md bg-light">
    <div class="container">
      <div @click="$router.push('/')" class="navbar-brand d-flex align-items-center pe-0">
        <div class="logo-header"></div>
        <span>STREAM Report</span>
      </div>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item dropdown" v-if="isAdmin">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Модерация
            </a>
            <div class="dropdown-menu">
              <router-link to="/employee" class="dropdown-item">Сотрудники</router-link>
              <router-link to="/student" class="dropdown-item">Студенты</router-link>
              <router-link to="/group" class="dropdown-item">Классы</router-link>
              <router-link to="/subject" class="dropdown-item">Предметы</router-link>
              <router-link to="/syllabus" class="dropdown-item">Учебные планы</router-link>
              <router-link to="/workload" class="dropdown-item">Нагрузка</router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Юниты
            </a>
            <div class="dropdown-menu">
              <router-link to="/myp" class="dropdown-item">Средняя школа</router-link>
              <!-- <router-link to="/dp" class="dropdown-item">Старшая школа</router-link> -->
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Оценивание
            </a>
            <div class="dropdown-menu">
              <!-- <router-link to="/assessment" class="dropdown-item">Итоговые работы</router-link> -->
              <!-- <router-link to="/schedule" class="dropdown-item">График работ</router-link> -->
              <router-link to="/report/teacher" class="dropdown-item">Репорты учителя</router-link>
              <router-link to="/report/psychologist" class="dropdown-item">Репорты психолога</router-link>
              <router-link to="/report/mentor" class="dropdown-item">Репорты наставника</router-link>
              <!-- <router-link to="/report/teacher" class="dropdown-item">Репорты учителя</router-link>
              <router-link to="/report/mentor" class="dropdown-item">Репорты наставника</router-link> -->
            </div>
          </li>
          <!-- <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Дополнительно
            </a>
            <div class="dropdown-menu">
              <router-link to="/extra/contest" class="dropdown-item">Олимпиады и конкурсы</router-link>
              <router-link to="/extra/teaching" class="dropdown-item">Педагогическое менторство</router-link>
            </div>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/unit" class="nav-link" aria-current="page">Юниты</router-link>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/assessment" class="nav-link">Оценки</router-link>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/report" class="nav-link">Репорты</router-link>
          </li> -->
        </ul>
        <div class="navbar-text d-flex align-items-center" v-if="authUser">
          <div class="navbar-user">
            <img :src='authUser.photo ? authUser.photo : require("@/assets/img/teacher.svg")' alt="" width="35" class="me-2">
            <div class="icon-online-dnevnik" v-if="isDnevnik"></div>
            <div v-else class="icon-offline-dnevnik"></div>
            <div class="navbar-user-name">
              <div v-if="authUser.last_name && authUser.first_name">
                {{ authUser.first_name }} {{ authUser.last_name }}
              </div>
              <div v-else>{{ authUser.username }}</div>
              <div class="navbar-user-sync" @click="getDataDnevnik" v-if="!isDnevnik" title="Нажмите и залогиньтесь в системе Дневник.ру">Синхронизировать с Дневник.ру</div>
            </div>
            
          </div>
          <button class="icon icon-logout" @click="logout"></button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'
const CLIEND_ID = '3097117bc2af450db4de47abe50d22ba'

export default {
  name: 'BaseNavbar',
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
    getDataDnevnik() {
      window.location.href = `https://login.dnevnik.ru/oauth2?response_type=token&client_id=${CLIEND_ID}&scope=CommonInfo,ContactInfo,EducationalInfo&redirect_uri=${window.location.href}&state=`;
    },
  },
  mounted() {
     
  },
  computed: {
    ...mapGetters(['authUser', 'isAdmin', 'isDnevnik']),
  }
}
</script>

<style scoped>
.navbar-user {
  display: flex;
  justify-content: flex-end;
  position: relative;
  align-items: center;
  min-width: 130px;
  margin-right: 5px;
}
.navbar-brand {
  cursor: pointer;
  font-family: 'Fira Sans', sans-serif;
}
.navbar-user-name {
  display: flex;
  flex-direction: column;
}
.navbar-user-sync {
  font-size: 0.6em;
  text-transform: uppercase;
  font-weight: 700;
}
.navbar-user-sync:hover {
  color: #674A9E;
  text-decoration: underline;
  cursor: pointer;
}
@media screen and (max-width: 768px) {
  .navbar-user {
    justify-content: flex-start;
  }
}
</style>