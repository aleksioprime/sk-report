<template>
  <div class="container">
    <footer class="footer-wrapper">
      <p class="col-md-4 mb-0 text-muted">&copy; 2022 ОЧУ МГ Сколково, Inc</p>
      <div class="logo-footer" @click="$router.push('/')"></div>
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

<style scoped>
.footer-wrapper {
  border-top: 1px solid var(--bs-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0 30px;
  flex-wrap: wrap;
  margin-top: 20px;
}

@media (max-width: 576px) {
  .footer-wrapper {
    flex-direction: column;
  }
}
</style>