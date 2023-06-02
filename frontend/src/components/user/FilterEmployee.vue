<template>
  <div class="block-filter">
    <div class="d-flex my-2">
      <input class="form-control" type="search" name="search" id="search" placeholder="Найти по фамилии..." v-model="searchValue" 
         @search="handleSearch">
      <button class="btn btn-primary ms-2" @click="handleSearch" :disabled="!searchValue">Найти</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {

  },
  data() {
    return {
      searchValue: null,
    }
  },
  methods: {
    handleSearch(event) {
      this.$emit('searchUser', this.searchValue)
    }
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
}
</style>