<template>
    <div class="login">
      <div class="form-signin w-100 m-auto">
        <form @submit.prevent="login">
          <img class="mb-3" src="@/assets/img/sk_report_logo_notext.svg" alt="" width="100">
          <h1 class="h3 mb-3 fw-normal">Войти в систему</h1>
          <div v-if="incorrectAuth" class="alert alert-danger">Вы ввели неправильный логин или пароль</div>
          <div class="form-floating">
            <input type="text" class="form-control" id="floatingInput" placeholder="Username"
                  v-model="username" />
            <label for="floatingInput">Пользователь</label>
          </div>
          <div class="form-floating">
            <input type="password" class="form-control" id="floatingPassword" placeholder="Password"
                  v-model="password" />
            <label for="floatingPassword">Пароль</label>
          </div>
          <!-- <div class="checkbox mb-3">
            <label for="rememberMe">
              <input id="rememberMe" type="checkbox" value="remember-me"> Запомнить меня
            </label>
          </div> -->
          <button class="w-100 btn btn-lg btn-primary" type="submit">Войти</button>
          <p class="mt-5 mb-3 text-muted">&copy; ОЧУ МГ Сколково 2022</p>
        </form>
      </div>
    </div>
  </template>
  
  <style>
  .login {
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding-top: 40px;
    padding-bottom: 40px;
    background-color: #f5f5f5;
    text-align: center;
  }
  .form-signin {
    max-width: 330px;
    padding: 15px;
  }
  
  .form-signin .form-floating:focus-within {
    z-index: 2;
  }
  
  .form-signin input[type="text"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }
  
  .form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
  </style>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        incorrectAuth: false,
      };
    },
    methods: { 
      async login() {
        await this.$store.dispatch('userLogin', {
          username: this.username,
          password: this.password,
        }).then(() => {
          this.$router.push({name: 'dashboard'})
        }).catch((error) => {
          console.log(error);
          this.incorrectAuth = true;
        })
      }
    },
    mounted() {
    },
  };
  </script>
  