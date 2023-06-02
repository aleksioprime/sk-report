
<template>
  <div class="block-container">
    <div class="selected-item">
      <div v-if="editableItem">
        <slot name="selected" :item="items.find(obj => obj.id == editableItem)"></slot>
      </div>
      <div v-else>Запись не выбрана</div>
    </div>
    <input id="search-item" class="form-control form-control-sm mb-2" type="search" v-model="queryItem"
      placeholder="Введите текст для поиска...">
    <div class="radiobutton-wrapper">
      <div v-for="item in foundItems" :key="item.id" class="radiobutton">
        <input type="radio" :value="item.id" :id="'item-' + item.id"
          v-model="editableItem" @change="changeOption">
        <label :for="'item-' + item.id">
          <slot name="found" :item="item"></slot>
        </label>
      </div>
      <!-- <div class="ms-2" v-if="foundItems.length > countItems">...</div> -->
    </div>
    <div class="ms-2" v-if="!foundItems.length">Ничего не найдено</div>
  </div>
</template>
  
<script>
export default {
  name: 'search-one-choice',
  props: {
    items: { type: Array, default: [] },
    editableItem: { type: Number },
    searchedField: { type: String, default: '' },
    countItems: { type: Number },
  },
  data() {
    return {
      queryItem: null,
    }
  },
  methods: {
    changeOption(event) {
      this.$emit('update:editableItem', this.editableItem);
    }
  },
  computed: {
    foundItems() {
      if (!this.queryItem) {
        // return this.items.filter((item, index) => {
        //   return this.editableItem == item.id
        // })
        return this.countItems ? this.items.slice(0, this.countItems) : this.items
      }
      const filteredItems = this.items.filter((item) => {
        if (item[`${this.searchedField}`]) {
          return item[`${this.searchedField}`].toLowerCase().includes(this.queryItem.toLowerCase()) || this.editableItem == item.id
        } else {
          return this.editableItem == item.id
        }
      })
      return this.countItems ? filteredItems.slice(0, this.countItems) : filteredItems
    },
  },
}
</script>

<style scoped>
.selected-item {
  padding: 5px 10px;
  border: 1px solid #674A9E;
  border-radius: 5px;
  font-weight: 700;
  margin-bottom: 10px;
}
.radiobutton-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  max-height: 200px;
  overflow-y: scroll;
}
.radiobutton label {
  padding: 5px;
  display: block;
}
.block-container {
  margin: 10px 0;
}
</style>