<template>
  <!-- Модальное окно -->
  <div class="modal fade" ref="modalUser" id="modalUser" data-bs-backdrop="static" data-bs-keyboard="false"
    tabindex="-1" aria-labelledby="modalUserLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalUserLabel">{{ modalTitle }}</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <slot name="body"></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
          <button v-if="flagUser.add" type="button" class="btn btn-primary" @click="$emit('create')">Добавить</button>
          <button v-if="flagUser.edit" type="button" class="btn btn-primary" @click="$emit('update')">Сохранить</button>
          <button v-if="flagUser.delete" type="button" class="btn btn-primary" @click="$emit('delete')">Удалить</button>
          <button v-if="flagUser.import" type="button" class="btn btn-primary" @click="$emit('import')">Загрузить</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'modal-user',
  props: {
    modalTitle: {
      type: String,
      default: 'Заголовок окна'
    },
    flagUser: {
      type: Object,
      default: {
        add: false,
        edit: false,
        delete: false,
      }
    }
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