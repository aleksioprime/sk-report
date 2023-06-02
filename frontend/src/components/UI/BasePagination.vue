<template>
  <nav aria-label="pagination" class="mt-3">
    <ul class="pagination">
      <!-- Ссылка на предыдущую страницу -->
      <li class="page-item" v-if="current != 1">
        <a class="page-link" href="#" aria-label="prev" @click="nextPage(current - 1)">
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>
      <!-- Ссылка на первую страницу -->
      <li class="page-item" v-if="current > range">
        <a class="page-link" href="#" aria-label="prev" @click="nextPage(1)">
          <span aria-hidden="true">1</span>
        </a>
      </li>
      <!-- Ссылка на предыдущую скрытую страницу -->
      <li class="page-item" v-if="current > range + 1">
        <a class="page-link" href="#" aria-label="prev" @click="nextPage(current - range)">
          <span aria-hidden="true">...</span>
        </a>
      </li>
      <!-- Ссылки на основной диапазон страниц -->
      <li class="page-item" v-for="page in total" :key="page"
        :class="{ 'active': current == page }">
        <a class="page-link" v-if="checkPage(page)" href="#" @click="nextPage(page)">{{ page }}</a>
      </li>
      <!-- Ссылка на следующую скрытую страницу -->
      <li class="page-item" v-if="current + range <= total - 1">
        <a class="page-link" href="#" aria-label="prev" @click="nextPage(current + range)">
          <span aria-hidden="true">...</span>
        </a>
      </li>
      <!-- Ссылка на последнюю страницу -->
      <li class="page-item" v-if="current + range <= total">
        <a class="page-link" href="#" aria-label="prev" @click="nextPage(total)">
          <span aria-hidden="true">{{ total }}</span>
        </a>
      </li>
      <!-- Ссылка на следующую страницу -->
      <li class="page-item" v-if="current != total">
        <a class="page-link" href="#" aria-label="next" @click="nextPage(current + 1)">
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </nav>
</template>
  
<script>
export default {
  name: 'base-pagination',
  props: {
    range: { type: Number },
    total: { type: Number },
    current: { type: Number },
  },
  methods: {
    nextPage(page) {
      console.log('Текущая страница: ', page)
      this.$emit('change', page)
    },
    checkPage(page) {
      return page > this.current - this.range && page < this.current + this.range
    }
  }
}
</script>
  
<style></style>