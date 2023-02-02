<template>
  <div class="d-flex py-1 px-1 user-item" @click="$emit('select', user)">
    <div class="me-3"><img :src='user.photo ? user.photo : require("@/assets/img/user.png")' alt="" width="50"></div>
    <div class="d-flex flex-column">
      <div class="user-name">{{ user.last_name }} {{ user.first_name }} {{ user.middle_name }}</div>
      <div>Пользователь: {{ user.username }} ({{ user.email }})</div>
      <div>Роли: <span v-for="role, index in user.role" :key="index"><span v-if="index != 0">, </span>{{ role.name }}</span>
      </div>
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
      backend: 'localhost:8000/'
    }
  },
  methods: {
  }
}
</script>

<style>
.user-item {
  cursor: pointer;
}

.user-item:hover {
  background-color: azure;
}

.user-name {
  text-transform: uppercase;
  font-weight: bold;
  color: rgb(61, 62, 63);
}
</style>