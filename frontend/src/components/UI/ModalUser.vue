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
          <slot name="footer"></slot>
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
      default: 'Заголовк окна'
    },
    flagUser: {
      type: Object,
      default: {
        addUser: false,
        editUser: false,
        deleteUser: false,
      }
    }
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
  mounted() {
    console.log('Dialog mounted');
    // this.modal = new Modal('#modalUser', { backdrop: 'static' });
  },
  watch: {

  }
}
</script>
  
<style scoped>

</style>