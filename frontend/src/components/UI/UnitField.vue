<template>
  <div class="unit-field">
    <div class="unit-field-label">{{ text.label }}</div>
    <div class="unit-field-data">
      <transition name="slide-fade">
        <div v-if="!fieldEdit">
          <div v-if="check"><slot name="read"></slot></div>
          <div v-else>Нет данных</div>
          <button class="unit-field-edtbtn" @click="editField"></button>
        </div>
        <div v-else>
          <div class="unit-field-description">{{ text.description }}</div>
          <div class="unit-field-warning">{{ text.warning }}</div>
          <slot name="edit"></slot>
          <button class="unit-field-done" @click="saveField">Сохранить</button>
          <button class="unit-field-cancel" @click="cancelField">Отмена</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'unit-field',
  props: {
    text: { type: Object, default: { title: '', description: '', warning: '' } },
    check: { type: Boolean },
  },
  data() {
    return {
      fieldEdit: false,
    }
  },
  methods: {
    saveField() {
      this.fieldEdit = false;
      this.$emit('save', true)
    },
    cancelField() {
      this.fieldEdit = false;
      this.$emit('cancel', true);
    },
    editField() {
      this.fieldEdit = true;
      this.$emit('edit', true);
    },
  },
  watch: {

  }
}
</script>