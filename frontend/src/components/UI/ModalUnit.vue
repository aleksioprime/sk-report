<template>
  <!-- Модальное окно -->
  <div class="modal fade" ref="modalUnit" id="modalUnit" data-bs-backdrop="static" data-bs-keyboard="false"
    tabindex="-1" aria-labelledby="modalUnitLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalUnitLabel">{{ modalTitle }}</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
          <button type="button" class="btn btn-primary" @click="$emit('create')">Добавить</button>
        </div>
      </div>
    </div>
  </div>
</template>
    
<script>
export default {
  name: 'modal-unit',
  props: {
    modalTitle: {
      type: String,
      default: 'Заголовок окна'
    },
    del: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      modal: {}
    }
  },
  methods: {
    hideDialog() {
      this.$emit('update:show', false)
    }
  },
  watch: {
  }
}
</script>
  
<style scoped>

</style>