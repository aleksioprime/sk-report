<template>
  <nav class="navbar navbar-expand-md bg-light mb-4">
    <div class="container">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand d-flex align-items-center" href @click="$router.push('/')"><img src="@/assets/img/logo.png"
          alt="" width="35" class="logo-rotate">SKReport</a>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/user')">
              Пользователи
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/unit')">
              Юниты
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/assess')">
              Оценки
            </a>
          </li>
        </ul>
      </div>
      <span class="navbar-text ms-3" v-if="user">
        Здравствуйте, {{ user.first_name }} {{ user.last_name.slice(0, 1) }}.
      </span>
      <span class="ms-2">
        <a class="nav-link" href="#" aria-current="page" @click="logout">
            Выход
          </a>
      </span>
          
    </div>
  </nav>
</template>

<script>

export default {
  name:  'BaseNavbar',
  props: ['user'],
  data() {
    return {
    };
  },
  methods: {
    logout() {
      this.axios.post('http://localhost:8080/api/v1/logout')
        .then(() => {
          this.setAuth(false);
          this.setUser({});
        })
        .catch(() => {
          console.log(error);
        });
    },
  },
  mounted() {
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