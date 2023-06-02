<template>
  <div>
    <base-header>
      <template v-slot:header>Cписок сотрудников</template>
    </base-header>
    <!-- Кнопки добавления, редактирования, удаления пользователей -->
    <div class="btn-wrapper">
      <button class="btn btn-primary" @click="showAddUser">Добавить сотрудника</button>
      <button class="btn btn-primary" @click="showImportUser" v-if="authUser.is_staff">Импорт</button>
      <div v-if="currentUser.id && !flagUser.add" class="icon-wrapper">
        <!-- <button type="button" class="icon icon-photo ms-2" @click="showEditPhoto"></button>
        <button type="button" class="icon icon-pass ms-2" @click="showEditPass"></button> -->
        <button type="button" class="icon icon-edit ms-4" @click="showEditUser"></button>
        <button type="button" class="icon icon-del ms-2" @click="showDelUser"></button>
        <!-- <button type="button" class="btn btn-primary ms-4" @click="showEditUser">Редактировать</button>
        <button type="button" class="btn btn-primary ms-2" @click="showDelUser">Удалить</button> -->
      </div>
    </div>
    <!-- Инструменты фильтрации сотрудников -->
    <filter-employee @searchUser="userSearch" />
    <!-- Список пользователей - учителей и администрации -->
    <div v-if="!isUserLoading" class="mt-3">
      <div>Всего сотрудников: <b>{{ totalUsers }}</b></div>
      <user-list :users="users"  @changePage="changePage" v-model:currentUser="currentUser"
        :totalPages="totalPages" :currentPage="currentPage" :flagUser="flagUser"/>
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <!-- Модальное окно добавления/редактирования/удаления пользователя -->
    <modal-user :modalTitle="modalTitle" @cancel="hideUserModal" :flagUser="flagUser"
      @create="userCreate" @update="userUpdate" @delete="userDelete" @import="userImport">
      <template v-slot:body>
        <form-employee ref="formEmployee" v-if="flagUser.add || flagUser.edit" :addMode="flagUser.add"
          v-model:editedUser="editedUser" v-model:validFormEmployee="validFormEmployee"/>
        <form-import v-if="flagUser.import" v-model="newUsers" />
        <div v-if="flagUser.delete">
          <div>Вы действительно хотите отправить этого сотрудника в архив?</div>
          <div class="user-delete">
            <div>{{ editedUser.last_name }} {{ editedUser.first_name }} {{ editedUser.middle_name }}</div>
            <div>Логин: {{ editedUser.username }}</div>
            <div>E-mail: {{ editedUser.email }}</div>
          </div>
        </div>
      </template>
    </modal-user>
  </div>
</template>

<script>
import UserList from "@/components/user/UserList";
import FormEmployee from "@/components/user/FormEmployee";
import FormImport from "@/components/user/FormImport";
import FilterEmployee from "@/components/user/FilterEmployee";
import { getUsers, createUser, updateUser, archiveUser, importUsers } from "@/hooks/user/useUser";
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';

export default {
  name: 'EmployeeBoard',
  components: {
    UserList, FilterEmployee, FormEmployee, FormImport
  },
  setup(props) {
    const { users, isUserLoading, totalPages, totalUsers, fetchGetUsers } = getUsers()
    const { fetchCreateUser } = createUser()
    const { fetchUpdateUser } = updateUser()
    const { fetchArchiveUser } = archiveUser()
    const { usersUpdated, isImportLoading, totalNewPages, totalNewUsers, fetchImportUsers } = importUsers()
    return {
      users, isUserLoading, totalPages, totalUsers, fetchGetUsers,
      fetchCreateUser, fetchUpdateUser, fetchArchiveUser,
      usersUpdated, isImportLoading, totalNewPages, totalNewUsers, fetchImportUsers
    }
  },
  data() {
    return {
      currentPage: 1,
      limit: 15,
      currentUser: {},
      editedUser: {},
      flagUser: {},
      modalTitle: '',
      validFormEmployee: false,
      searchValue: null,
      newUsers: [],
    }
  },
  methods: {
    // Выбор текущей страницы
    changePage(page) {
      this.currentPage = page;
      this.fetchGetUsers({ role: "teacher", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    // Открытие модального окна для добавления сотрудника 
    showAddUser() {
      this.modalTitle = "Добавление сотрудника";
      this.flagUser.add = true;
      this.editedUser = {
        teacher: {}
      };
      this.modalUser.show();
    },
    showImportUser() {
      this.modalTitle = 'Импорт сотрудников';
      this.flagUser.import = true;
      this.modalUser.show();
    },
    // Открытие модального окна для редактирования сотрудника 
    showEditUser() {
      this.modalTitle = "Редактирование сотрудника";
      this.editedUser = { ...this.currentUser }
      this.editedUser.teacher = { ...this.currentUser.teacher }
      this.flagUser.edit = true;
      this.modalUser.show();
    },
    // Открытие модального окна для удаления сотрудника 
    showDelUser() {
      this.modalTitle = "Удаление сотрудника";
      this.editedUser = { ...this.currentUser }
      this.flagUser.delete = true;
      this.modalUser.show();
    },
    // Закрытие модального окна
    hideUserModal() {
      this.validFormEmployee = false;
      this.editedUser = {};
      this.modalUser.hide();
      this.flagUser = {};
    },
    // Валидация формы и отправка запроса на добавления сотрудника
    userCreate() {
      this.$refs.formEmployee.checkFieldsValidate();
      if (this.validFormEmployee) {
        console.log("Запрос на создание пользователя: ", this.editedUser);
        this.fetchCreateUser(this.editedUser).then(() => {
          this.hideUserModal();
          this.fetchGetUsers({ role: "teacher", page: this.currentPage, limit: this.limit }).finally(() => {
            this.currentUser = {};
          });
        })
      } else {
        console.log('Валидация неуспешна', this.currentUser)
      }
    },
    // Валидация формы и отправка запроса на обновление информации о сотруднике
    userUpdate() {
      this.$refs.formEmployee.checkFieldsValidate();
      if (this.validFormEmployee) {
        delete this.editedUser.student;
        console.log("Запрос на обновление пользователя: ", this.editedUser);
        this.fetchUpdateUser(this.editedUser).then(() => {
          this.hideUserModal();
          this.fetchGetUsers({ role: "teacher", search: this.searchValue, page: this.currentPage, limit: this.limit }).finally(() => {
            this.currentUser = this.users.find(item => item.id == this.currentUser.id);
          });
        });
      } else {
        console.log('Валидация неуспешна', this.currentUser)
      }
    },
    // Валидация формы и отправка запроса на удаление сотруднике
    userDelete() {
      delete this.editedUser.student;
      this.fetchArchiveUser(this.editedUser).then(() => {
        this.hideUserModal();
        this.fetchGetUsers({ role: "teacher", page: this.currentPage, limit: this.limit }).finally(() => {
          this.currentUser = {};
        });
      });
    },
    userImport() {
      console.log(this.newUsers)
      const data = {
        'users': this.newUsers,
        'role': 'teacher',
      }
      this.fetchImportUsers(data, this.limit).then(() => {
        this.users = [ ...this.usersUpdated ];
        this.isUserLoading = this.isImportLoading;
        this.totalUsers = this.totalNewUsers;
        this.totalPages = this.totalNewPages;
        this.currentPage = 1,
        this.hideUserModal();
      }).finally(() => {
        this.currentUser = {};
      });
    },
    // Поиск учителя по фамилии
    userSearch(search) {
      this.currentPage = 1;
      this.searchValue = search;
      this.fetchGetUsers({ role: "teacher", search: search, limit: this.limit });
    }
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalUser = new Modal('#modalUser', { backdrop: 'static' });
    // Запросы данных при загрузке страницы
    this.fetchGetUsers({ role: "teacher", page: this.currentPage, limit: this.limit });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.btn-wrapper {
  top: 0;
  position: sticky;
  display: flex;
  padding: 10px;
  background: #ffffff;
  z-index: 2;
}
.icon-wrapper {
  display: flex;
  margin-left: auto;
}
</style>