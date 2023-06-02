<template>
  <div class="user-item" @click="$emit('select', user)">
    <div class="user-photo me-3">
      <img :src='user.photo ? user.photo : require("@/assets/img/teacher.svg")' alt="" width="50">
      <div v-if="user.teacher && user.teacher.admin" class="icon-admin"></div>
    </div>
    <div class="d-flex flex-column">
      <div class="user-name">
        <h4>{{ user.last_name }} {{ user.first_name }} {{ user.middle_name }}</h4></div>
      <div>Пользователь: {{ user.username }} ({{ user.email }})</div>
      <div v-if="user.teacher">{{ user.teacher.position }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      
    }
  },
  methods: {
    getGroupStudent(groups) {
      return groups.find(item => item.study_year == 1) || {}
    }
  }
}
</script>

<style>
.user-item {
  cursor: pointer;
  display: flex;
}
.user-name {
  text-transform: uppercase;
  font-weight: bold;
  color: rgb(61, 62, 63);
}
.user-photo {
  position: relative;
}
</style>