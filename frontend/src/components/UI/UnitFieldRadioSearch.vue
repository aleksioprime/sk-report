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
          <input id="search-item" class="form-control mb-2" type="text" v-model="search" placeholder="Введите текст для поиска...">
          <div v-for="op in searchOptions.slice(0, 5)" :key="op.id">
            <div class="form-check ms-3">
              <input class="form-check-input" type="radio" :name="fieldName" :value="op.id" :id="fieldName + '-' + op.id"
                v-model="editData[`${fieldName}_id`]">
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
  name: 'unit-field-radio-search',
  props: {
    fieldName: { String },
    fieldText: { Object },
    fieldData: { type: Object },
    options: { type: Array, default: () => [] },
    fieldSearch: { type: String, default: ''},
  },
  setup(props) {
    return {

    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
      search: null,
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
      this.editData[`${this.fieldName}_id`] = this.fieldData ? this.fieldData.id : null;
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
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchAuthors)
    searchOptions() {
      if (!this.search) {
        return this.options.filter((item, index) => {
           return (index <= 5) || this.editData[`${this.fieldName}_id`] == item.id || item.id == null
          })
      }
      return this.options.filter((item) => {
        if (item[this.fieldSearch]) {
          return item[this.fieldSearch].toLowerCase().includes(this.search.toLowerCase()) || this.editData[`${this.fieldName}_id`] == item.id || item.id == null
        } else {
          return this.editData[`${this.fieldName}_id`] == item.id || item.id == null
        }
      })
    }
  },
}
</script>