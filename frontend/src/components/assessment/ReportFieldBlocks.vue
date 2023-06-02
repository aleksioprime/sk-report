<template>
  <div class="unit-field my-2">
    <div class="block-wrapper" v-if="checkData">
      <div v-for="item in fieldData" :key="item.id">
        <div class="block-item">
          <slot name="show" :data="item"></slot>
          <div class="field-btn-wrapper" v-if="editable && !createMode && !editingItemID && !deletingItemID">
            <button class="icon icon-edit" @click="showEditForm(item.id)"></button>
            <button class="icon icon-del" @click="showDeleteForm(item.id)"></button>
          </div>
        </div>
        <transition name="slide-fade">
          <div class="mt-2 p-2 border" v-if="editingItemID == item.id">
            <div class="block-heading">Редактирование записи</div>
            <slot name="form" :data="editItem"></slot>
            <div class="d-flex justify-content-end">
              <button class="btn btn-success" @click="editConfirmUpdate">ОК</button>
              <button class="btn btn-cancel" @click="editCancel">Отмена</button>
            </div>
          </div>
        </transition>
        <transition name="slide-fade">
          <div class="mt-2 p-2 border" v-if="deletingItemID == item.id">
            <div class="block-heading">Удаление записи</div>
            Вы действительно хотите удалить эту запись?
            <div class="d-flex justify-content-end">
              <button class="btn btn-success" @click="editConfirmDelete">ОК</button>
              <button class="btn btn-cancel" @click="editCancel">Отмена</button>
            </div>
          </div>
        </transition>
      </div>
    </div>
    <div v-else class="block-none">
      Нет записей
    </div>
    <button class="my-2 btn btn-primary" @click="showAddForm"
      v-if="editable && !createMode && !editingItemID && !deletingItemID">Добавить</button>
    <transition name="slide-fade">
      <div class="mt-2 p-2 border" v-if="createMode">
        <div class="block-heading">Добавление записи</div>
        <slot name="form" :data="editItem"></slot>
        <div class="d-flex justify-content-end">
          <button class="btn btn-success" @click="editConfirmCreate">ОК</button>
          <button class="btn btn-cancel" @click="editCancel">Отмена</button>
        </div>
      </div>
    </transition>
  </div>
</template>
  
<script>
export default {
  name: 'ReportFieldBlocks',
  props: {
    fieldName: { String },
    fieldText: { Object },
    fieldData: { type: Array },
    checkLine: { type: Boolean, default: false },
    defaultItem: { type: Object, default: {} },
    editable: { type: Boolean, default: false },
  },
  setup(props) {
    return {

    }
  },
  data() {
    return {
      editMode: false,
      editField: {},
      editItem: {},
      createMode: false,
      editingItemID: null,
      deletingItemID: null,
    }
  },
  methods: {
    getKeys(item) {
      let keys = {}
      for (let key in item) {
        if (!item[key]) {
          continue
        }
        if (typeof item[key] === 'object' && 'id' in item[key]) {
          keys[`${key}_id`] = item[key].id
        } else if (Array.isArray(item[key])) {
          keys[`${key}_ids`] = item[key].map(item => item.id)
        } else {
          keys[key] = item[key]
        }
      }
      return keys
    },
    cancelField() {
      this.editMode = false;
    },
    editingField() {
      this.editMode = true;
      this.$emit('edit', this.fieldName);
    },
    showAddForm() {
      this.createMode = true;
      this.editItem = { ...this.defaultItem }
    },
    showEditForm(id) {
      this.editingItemID = id;
      this.editItem = this.getKeys({ ...this.fieldData.find(item => item.id == id) })
    },
    showDeleteForm(id) {
      this.deletingItemID = id;
    },
    editConfirmCreate() {
      this.editField[`${this.fieldName}`] = this.fieldData.map(item => this.getKeys(item));
      this.editField[`${this.fieldName}`].push(this.editItem)
      this.$emit('save', this.editField)
      console.log(this.editField)
      this.createMode = false;
      this.editItem = {};
    },
    editConfirmUpdate() {
      this.editField[`${this.fieldName}`] = this.fieldData.map(item => {
        if (item.id == this.editItem.id) {
          return this.editItem
        } else {
          return this.getKeys(item)
        }
      });
      this.$emit('save', this.editField)
      console.log(this.editField)
      this.editingItemID = null;
      this.editItem = {};
    },
    editConfirmDelete() {
      this.editField[`${this.fieldName}`] = this.fieldData.map(item => this.getKeys(item)).filter(item => item.id != this.deletingItemID);
      this.$emit('save', this.editField);
      console.log(this.editField)
      this.deletingItemID = null;
    },
    editCancel() {
      this.createMode = false;
      this.editingItemID = null;
      this.deletingItemID = null;
      this.editItem = {};
    }
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
    this.editItem = {}
  },
  watch: {

  }
}
</script>