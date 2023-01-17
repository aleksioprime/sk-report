<template>
  <div class="container">
    <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
      <p class="col-md-4 mb-0 text-muted">&copy; 2022 ОЧУ МГ Сколково, Inc</p>

      <a href="/" class="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
        <img src="@/assets/img/skreport.png" alt="" height="35">
      </a>

      <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
        <li class="ms-3"><img src="@/assets/img/vk.png" class="bi" width="24" height="auto" alt="vk" /></li>
        <li class="ms-3"><img src="@/assets/img/telegram.png" class="bi" width="24" height="auto" alt="tg" /></li>
      </ul>
    </footer>
  </div>
</template>

<script>
export default {
  name:  'BaseFootbar',
}
</script>

<style>

</style>