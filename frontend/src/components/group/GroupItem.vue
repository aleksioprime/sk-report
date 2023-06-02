<template>
  <div class="group-item" @click="$emit('select', group)">
    <div>{{ group.class_year.year_rus }}{{ group.letter }} класс</div>
    <div class="btn-wrapper" v-if="showEditButton">
      <button class="icon icon-edit" @click="$emit('update', group)"></button>
      <button class="icon icon-del" @click="$emit('delete', group)"></button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    group: {
      type: Object,
      required: true,
    },
    showEditButton: {
      type: Boolean,
      default: false,
    }
  },
}
</script>

<style>
.group-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 10px;
}
.group-item:hover {
  background: #ebebeb;
}
.btn-wrapper {
  margin-left: auto;
  display: flex;
  align-items: center;
}
</style>