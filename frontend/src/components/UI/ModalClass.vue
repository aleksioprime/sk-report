<template>
  <!-- Модальное окно -->
  <div class="modal fade" ref="modalClass" id="modalClass" data-bs-backdrop="static" data-bs-keyboard="false"
    tabindex="-1" aria-labelledby="modalClassLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalClassLabel">{{ modalTitle }}</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
          <button type="button" class="btn btn-primary" @click="$emit('save')">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'modal-class',
  props: {
    modalTitle: {
      type: String,
      default: 'Заголовок окна'
    },
  },
  data() {
    return {
      modal: {}
    }
  },
  methods: {

  },
  mounted() {

  },
  watch: {

  }
}
</script>
  
<style scoped>

</style>