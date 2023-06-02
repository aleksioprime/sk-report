<template>
  <!-- Модальное окно -->
  <div class="modal fade" :ref="modalId" :id="modalId" data-bs-backdrop="static" data-bs-keyboard="false"
    tabindex="-1" :aria-labelledby="`${modalId}Label`" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" :id="`${modalId}Label`">{{ modalTitle }}</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
          <button v-if="flagUnit.add" type="button" class="btn btn-primary" @click="$emit('create')">Добавить</button>
          <button v-if="flagUnit.delete" type="button" class="btn btn-primary" @click="$emit('delete')">Удалить</button>
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
    flagUnit: {
      type: Object,
      default: {
        add: false,
        edit: false,
        delete: false,
      }
    },
    modalId: {
      type: String,
      default: 'modalUnit',
    }
  },
  data() {
    return {
    }
  },
  methods: {
  },
  watch: {
  }
}
</script>
  
<style scoped>

</style>