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
              <div>{{ fieldData }}</div> 
            </div>
            <div v-else>Нет данных</div>
          </div>
          <div v-else>
            <div class="field-description">{{ fieldText.description }}</div>
            <div class="field-warning">{{ fieldText.warning }}</div>
            <input class="form-control" type="text" v-model="editData[fieldName]">
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
    name: 'unit-field-string',
    props: {
      fieldName: { String },
      fieldText: { Object },
      fieldData: { Object },
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
        this.editData[this.fieldName] = this.fieldData;
      },
    },
    computed: {
      checkData() {
        if (Array.isArray(this.fieldData)) {
          return Boolean(this.fieldData.length)
        } else  {
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