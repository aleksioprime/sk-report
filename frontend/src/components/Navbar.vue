<template>
  <nav class="navbar navbar-expand-md bg-light mb-4">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href @click="$router.push('/')"><img src="@/assets/img/logo.png" alt="" width="35" class="logo-rotate">SKReport</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/userlist')">
              Пользователи
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/unitplans')">
              Юниты
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" aria-current="page" @click="$router.push('/assessment')">
              Оценки
            </a>
          </li>
        </ul>
      </div>
      <span class="navbar-text ms-3">
        Здравствуйте, пользователь.
      </span>
      <ul class="navbar-nav ms-auto mb-2 mb-md-0">
        <li class="nav-item">
          <a class="nav-link" href aria-current="page" @click="$router.push('/')">
            Выход
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {

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