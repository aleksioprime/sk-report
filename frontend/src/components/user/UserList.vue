<template>
  <div v-if="users.length > 0" ref="userlist">
    <!-- Список пользователь -->
    <transition-group name="user-list">
      <user-item v-for="user in users" :key="user.id" :user="user" @select="userSelect"
        :class="[currentUser == user ? 'selected' : '']" class="area" />
    </transition-group>
    <!-- Нумерация страниц -->
    <base-pagination :total="totalPages" :current="currentPage" :range="4" @change="nextPage"/>
  </div>
  <div v-else>
    Список пользователей пуст
  </div>
</template>

<script>
import UserItem from "@/components/user/UserItem";
export default {
  name: 'UserList',
  components: {
    UserItem
  },
  props: {
    users: {
      type: Array,
      required: true,
      default: [],
    },
    totalPages: {
      type: Number,
      default: 1,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
    currentUser: {
      type: Object,
      default: {},
    },
    flagUser: {
      type: Object,
      default: {}
    },
  },
  data() {
    return {

    }
  },
  methods: {
    // Выбор текущего пользователя при нажатии на строку списка
    userSelect(user) {
      if (this.currentUser != user) {
        this.$emit('update:currentUser', user);
      } else {
        this.$emit('update:currentUser', {});
      }
    },
    userUnSelect(event) {
      if (event.type == 'keydown') {
        if (event.key == 'Escape' && !Object.keys(this.flagUser).length) {
          this.$emit('update:currentUser', {});
        }
      }
    },
    nextPage(page) {
      this.$emit('changePage', page)
    },
  },
  mounted() {
    window.addEventListener('keydown', this.userUnSelect);
    document.addEventListener('click', this.userUnSelect);
  }
}
</script>

<style>
.selected {
  background: #DBEDEB;
}
</style>