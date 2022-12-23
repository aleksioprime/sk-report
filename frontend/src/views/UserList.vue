<template>
  <div>
    <h1 class="mb-2">Cписок пользователей</h1>
    <!-- Поля сортировки и фильтрации пользователей -->
    <div class="row">
      <div class="col d-flex align-items-end">
        <input class="form-control me-2" type="text" name="search" id="search" placeholder="Найти по фамилии..."
          v-model="searchQuery">
      </div>
      <div class="col-4">
        <label for="sorted">Сортировка</label>
        <select id="sorted" class="form-select" v-model="selectedSort">
          <option disabled value="">Выберите из списка</option>
          <option v-for="option in sortOptions" :key="option.value" :value="option.value">{{ option.name }}</option>
        </select>
      </div>
    </div>
    <!-- Кнопки добавления/редактирования/удаления пользователя -->
    <div class="d-flex flex-wrap" ref="tools">
      <button type="button" class="btn btn-primary my-3" @click="showModalUserAdd">
        Добавить пользователя
      </button>
      <button v-if="Object.keys(currentUser).length" type="button" class="btn btn-primary my-3 ms-auto"
        @click="showModalUserEdit">
        Редактировать
      </button>
      <button v-if="Object.keys(currentUser).length" type="button" class="btn btn-primary my-3 ms-2"
        @click="showModalUserDelete">
        Удалить
      </button>
    </div>
    <!-- Модальное окно добавления/редактирования/удаления пользователя -->
    <modal-user :modalTitle="modalTitle" :flagUser="flagUser" @cancel="hideModalUser">
      <template v-slot:body>
        <user-form v-if="flagUser.addUser || flagUser.editUser" :user="currentUser" />
        <user-delete v-if="flagUser.deleteUser" :user="currentUser" />
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-secondary" @click="hideModalUser()">Отмена</button>
        <button v-if="flagUser.addUser" type="button" class="btn btn-primary">Добавить</button>
        <button v-if="flagUser.editUser" type="button" class="btn btn-primary">Сохранить</button>
        <button v-if="flagUser.deleteUser" type="button" class="btn btn-primary">Удалить</button>
      </template>
    </modal-user>
    <!-- Список пользователей -->
    <div v-if="displayUsers.length > 0" ref="userlist">
      <transition-group name="user-list">
        <user-item v-for="user in displayUsers" :key="user.id" :user="user" @select="selectUser"
          :class="[currentUser == user ? 'select-user' : '']" />
      </transition-group>
      <nav aria-label="pagination" class="mt-3">
        <ul class="pagination">
          <li class="page-item">
            <a class="page-link" href="#" aria-label="prev" @click="currentPage--">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item" v-for="pageNumber in totalPages" :key="pageNumber">
            <a class="page-link" href="#" @click="changePage(pageNumber)">{{ pageNumber }}</a>
          </li>
          <li class="page-item">
            <a class="page-link" href="#" aria-label="next" @click="currentPage++">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </nav>
    </div>
    <div v-else>
      Список пользователей пуст
    </div>
  </div>
</template>

<script>
import UserForm from "@/components/UserForm.vue";
import UserDelete from "@/components/UserDelete.vue";
import UserItem from "@/components/UserItem";
import { Modal } from 'bootstrap';
import { useUsers } from "@/hooks/useUsers";
import { useSortedUsers } from "@/hooks/useSortedUsers";
import { useSortedAndSearchUsers } from "@/hooks/useSortedAndSearchUsers";

export default {
  name: 'UserList',
  components: {
    UserForm, UserDelete, UserItem
  },
  setup(props) {
    const { users } = useUsers();
    const { sortedUsers, selectedSort } = useSortedUsers(users);
    const { searchQuery, sortedAndSearchUsers } = useSortedAndSearchUsers(sortedUsers);
    return {
      users,
      selectedSort,
      searchQuery,
      sortedAndSearchUsers,
    }
  },
  data() {
    return {
      modalUser: {},
      modalTitle: '',
      flagUser: {
        addUser: false,
        editUser: false,
        deleteUser: false,
      },
      currentUser: {},
      sortOptions: [
        { value: 'last_name', name: 'По фамилии' },
        { value: 'first_name', name: 'По имени' },
      ],
      currentPage: 1,
      pageSize: 5,
      totalPages: 1,
    }
  },
  methods: {
    showModalUserAdd() {
      this.modalTitle = 'Регистрация пользователя';
      this.flagUser.addUser = true;
      this.currentUser = {};
      this.modalUser.show();
    },
    showModalUserEdit() {
      this.modalTitle = 'Редактирование пользователя';
      this.flagUser.editUser = true;
      this.modalUser.show();
    },
    showModalUserDelete() {
      this.modalTitle = 'Удаление пользователя';
      this.flagUser.deleteUser = true;
      this.modalUser.show();
    },
    hideModalUser() {
      this.modalUser.hide();
      this.flagUser = {
        addUser: false,
        editUser: false,
        deleteUser: false,
      }
    },
    selectUser(user) {
      this.currentUser = user;
    },
    unSelectUser(event) {
      if (event.type == 'keydown') {
        if (event.key == 'Escape' && !(this.flagUser.editUser || this.flagUser.deleteUser)) {
          this.currentUser = {};
        }
      } else if (event.type == 'click') {
        if (this.$refs.userlist) {
          if (!(this.$refs.userlist.contains(event.target) || this.$refs.tools.contains(event.target)) &&
          !(this.flagUser.editUser || this.flagUser.deleteUser)) {
            this.currentUser = {};
          }
        }
      }
    },
    changePage(pageNumber) {
      this.currentPage = pageNumber
    },
  },
  mounted() {
    this.modalUser = new Modal('#modalUser', { backdrop: 'static' });
    window.addEventListener('keydown', this.unSelectUser);
    document.addEventListener('click', this.unSelectUser);
  },
  computed: {
    // функция пагинации результирующего списка пользователей для постраничного вывода на экран
    displayUsers() {
      this.totalPages = Math.ceil( this.sortedAndSearchUsers.length / this.pageSize);
      const startSlice = this.pageSize * (this.currentPage - 1);
      const endSlice = this.currentPage * this.pageSize;
      return this.sortedAndSearchUsers.slice(startSlice, endSlice);
    },
  }, 
  watch: {
    // наблюдение за текущей страницей пагинации 
    // если меньше нуля, то = 1, если больше последней, то = последней
    currentPage() {
      if (this.currentPage <= 0) {
        this.currentPage = 1;
      } else if (this.currentPage > this.totalPages) {
        this.currentPage = this.totalPages;
      }
    }
  }
}
</script>

<style scoped>
.select-user {
  background-color: rgb(161, 161, 161) !important;
}

.user-list-item {
  display: inline-block;
  margin-right: 10px;
}

.user-list-enter-active, .user-list-leave-active {
  transition: all 0.4s ease;
}

.user-list-enter-from, .user-list-leave-to {
  opacity: 0;
  transform: translateX(130px);
}

.user-list-move {
  transition: transform 0.4s ease;
}
</style>