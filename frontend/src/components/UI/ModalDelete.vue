<template>
    <!-- Модальное окно -->
    <div class="modal fade" :ref="'modalDelete'+idName" :id="'modalDelete'+idName" data-bs-backdrop="static" data-bs-keyboard="false"
      tabindex="-1" :aria-labelledby="'modalDelete'+idName+'Label'" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" :id="'modalDelete'+idName+'Label'">{{ modalTitle }}</h5>
            <button type="button" class="btn-close" @click="$emit('cancel')" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <slot></slot>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
            <button v-if="del" type="button" class="btn btn-danger" @click="$emit('delete')">Удалить</button>
            <button v-else type="button" class="btn btn-primary" @click="$emit('create')">Добавить</button>
          </div>
        </div>
      </div>
    </div>
  </template>
      
  <script>
  export default {
    name: 'modal-delete',
    props: {
      modalTitle: {
        type: String,
        default: 'Подтвердите удаление записи'
      },
      del: {
        type: Boolean,
        default: false
      },
      idName: {
        type: String,
        default: 'Item'
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