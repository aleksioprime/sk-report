<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">{{ fieldText.label }}</div>
      <button v-if="!editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div v-if="checkData">
            <slot name="show" :data="fieldData"></slot>
          </div>
          <div v-else>Нет данных</div>
        </div>
        <div v-else>
          <div class="field-description">{{ fieldText.description }}</div>
          <div class="field-warning">{{ fieldText.warning }}</div>
          <div v-for="op in options" :key="op.id">
            <div class="form-check ms-3">
              <input class="form-check-input" type="radio" :name="fieldName" :value="op.id" :id="fieldName + '-' + op.id" v-model="editData[`${fieldName}_id`]">
              <label class="form-check-label" :for="fieldName + '-' + op.id">
                <slot name="edit" :data="op"></slot>
              </label>
            </div>
          </div>
          <div class="field-buttons">
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'unit-field-radio',
  props: {
    fieldName: { String },
    fieldText: { Object },
    fieldData: { Object },
    options: { type: Array, default: () => [] },
  },
  setup(props) {
    return {

    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
    }
  },
  methods: {
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData)
    },
    cancelField() {
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      if (this.fieldData) {
        this.editData[`${this.fieldName}_id`] = this.fieldData.id;
      } else {
        this.editData[`${this.fieldName}_id`] = []
      }
      this.$emit('edit', this.fieldName);
    },
  },
  computed: {
    checkData() {
      if (Array.isArray(this.fieldData)) {
        return Boolean(this.fieldData.length)
      } else {
        return Boolean(this.fieldData)
      }
    },
  },
  mounted() {
  },
  watch: {

  }
}
</script>