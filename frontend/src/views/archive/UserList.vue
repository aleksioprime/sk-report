<template>
  <div>
    <base-header>
      <template v-slot:header>Cписок пользователей</template>
    </base-header>
    <!-- Кнопки добавления/редактирования/удаления пользователя -->
    <div class="d-flex flex-wrap align-items-center" ref="tools">
      <button type="button" class="btn btn-primary my-3" @click="addUserButton">
        Добавить пользователя
      </button>
      <button type="button" class="img-btn-import ms-2" @click="importUserButton"></button>
      <div v-if="Object.keys(currentUser).length && !flagUser.addUser" class="my-3 d-flex align-items-center ms-auto">
        <!-- <button type="button" class="img-btn-photo ms-2" @click="editPhotoButton"></button>
        <button type="button" class="img-btn-pass ms-2" @click="editPasswordButton"></button> -->
        <!-- <button type="button" class="img-btn-edit ms-4" @click="editUserButton"></button>
        <button type="button" class="img-btn-del ms-2" @click="deleteUserButton"></button> -->
        <button type="button" class="btn btn-primary ms-4" @click="editUserButton">Редактировать</button>
        <button type="button" class="btn btn-primary ms-2" @click="deleteUserButton">Удалить</button>
      </div>
    </div>
    <!-- Модальное окно добавления/редактирования/удаления пользователя -->
    <modal-user :modalTitle="modalTitle" :flagUser="flagUser" @cancel="userCancel"
      @create="userCreate" @update="userUpdate" @delete="userDelete" @import="userImport">
      <template v-slot:body>
        <!-- Форма добавления/редактирования пользователя -->
        <!-- checkValid - флаг необходимости проверки формы,  validForm - сигнал успешности проверки формы  -->
        <user-form v-if="flagUser.addUser || flagUser.editUser" v-model="currentUser" :roles="roles" :groups="groups"
          :addMode="flagUser.addUser" :checkValid="checkValid" @validForm="validFormResult" />
        <user-import-form v-if="flagUser.import" v-model="newUsers" />
        <div v-if="flagUser.deleteUser">Вы действительно хотите удалить этого пользователя?</div>
      </template>
    </modal-user>
    <transition name="fade">
    <div class="row" v-show="showUsersData">
      <div class="col-md-3">
        <div class="d-flex my-2">
          <input class="form-control" type="text" name="search" id="search" placeholder="Найти по фамилии..."
            v-model="searchLastName">
        </div>
        <div class="my-2">
          <select id="sorted" class="form-select" v-model="selectedSortUser">
            <option disabled value="">Сортировка</option>
            <option v-for="option in sortUserOptions" :key="option.value" :value="option.value">{{ option.name }}
            </option>
          </select>
        </div>
        <div class="flex-md-column align-items-center align-items-md-start flex-wrap my-2">
          <div class="form-check">
            <input class="form-check-input" type="radio" name="role" :value="null" :id="'role-x'" v-model="queryRole"
              @change="refreshUsers">
            <label class="form-check-label" :for="'role-x'">
              Все роли
            </label>
          </div>
          <div v-for="rl in roles" :key="rl.id" class="me-2">
            <div class="form-check">
              <input class="form-check-input" type="radio" name="role" :value="rl.id" :id="'role-' + rl.id"
                v-model="queryRole" @change="refreshUsers">
              <label class="form-check-label" :for="'role-' + rl.id">
                {{ rl.name }}
              </label>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md">
        <!-- Список пользователей -->
        <div v-if="displayUsers.length > 0" ref="userlist">
          <div>Всего пользователей: <b>{{ users.length }}</b></div>
          <transition-group name="user-list">
            <user-item v-for="user in displayUsers" :key="user.id" :user="user" @select="selectUser"
              :class="[currentUser == user ? 'select-user' : '']" class="border my-1"/>
          </transition-group>
          <nav aria-label="pagination" class="mt-3">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="prev" @click="currentPage--">
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>
              <li class="page-item" v-for="pageNumber in totalPages" :key="pageNumber" :class="{ 'active' : currentPage == pageNumber }">
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
    </div>
    </transition>
  </div>
</template>

<script>
import UserForm from "@/components/UserForm";
import UserImportForm from "@/components/user/UserImportForm";
import UserItem from "@/components/user/UserItem";
import { Modal } from 'bootstrap';

import { getUsers, getRoles, getGroups } from "@/hooks/user/getUserData";
import { useSortingUsers, filterUsersByLastName, getRolesFromUsers } from "@/hooks/user/filterUserData";

export default {
  name: 'UserList',
  components: {
    UserForm, UserItem, UserImportForm
  },
  setup(props) {
    const { users, getUserData } = getUsers()
    const { roles, getRolesData } = getRoles();
    const { groups, getGroupsData } = getGroups();
    const { sortedUsers, selectedSortUser } = useSortingUsers(users);
    const { searchLastName, foundUsers } = filterUsersByLastName(sortedUsers);
    const { rolesFromUsers } = getRolesFromUsers(sortedUsers);
    return {
      users, getUserData,
      roles, getRolesData,
      groups, getGroupsData,
      sortedUsers, selectedSortUser,
      searchLastName, foundUsers,
      rolesFromUsers
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
        import: false,
      },
      currentUserDefault: {
        roles_ids: [],
        student: {},
        teacher: {},
      },
      currentUser: {},
      newUsers: [],
      sortUserOptions: [
        { value: 'last_name', name: 'По фамилии' },
        { value: 'first_name', name: 'По имени' },
      ],
      currentPage: 1,
      pageSize: 10,
      totalPages: 1,
      checkValid: false,
      validForm: false,
      queryRole: null,
      showUsersData: false,
    }
  },
  methods: {
    // Запрос пользователей по выбранной роли
    refreshUsers() {
      this.getUserData({ role: this.queryRole });
    },
    // Получение результатов валидации из компонента с формой
    validFormResult(value) {
      this.validForm = value;
    },
    // Нажатие на кнопку добавления пользователя
    addUserButton() {
      this.modalTitle = 'Регистрация пользователя';
      this.getRolesData();
      this.getGroupsData();
      this.flagUser.addUser = true;
      this.currentUser = { ...this.currentUserDefault };
      this.modalUser.show();
    },
    // Нажатие на кнопку редактирования пользователя
    editUserButton() {
      this.modalTitle = 'Редактирование пользователя';
      this.getRolesData();
      this.getGroupsData();
      console.log(this.currentUser)
      this.currentUser.roles_ids = this.currentUser.role.map(item => item.id)
      if (!this.currentUser.student) {
        this.currentUser.student = {
          group_id: null,
        }
      }
      if (!this.currentUser.teacher) {
        this.currentUser.teacher = {}
      }
      if (this.currentUser.roles_ids.includes(1) && this.currentUser.student.group) {
        this.currentUser.student.group_id = this.currentUser.student.group.id;
      }
      this.flagUser.editUser = true;
      this.modalUser.show();
    },
    // Нажатие на кнопку удаления пользователя
    deleteUserButton() {
      this.modalTitle = 'Удаление пользователя';
      this.flagUser.deleteUser = true;
      this.modalUser.show();
    },
    // Нажатие на кнопку изменения фотографии пользователя
    editPhotoButton() {

    },
    // Нажатие на кнопку изменения пароля пользователя
    editPasswordButton() {

    },
    // Нажатие на кнопку импорта пользователя
    importUserButton() {
      this.modalTitle = 'Импорт пользователей';
      this.flagUser.import = true;
      this.modalUser.show();
    },
    // Срабатывание сигнала отмены действия над пользователем и закрытие модульного окна
    userCancel() {
      this.checkValid = false;
      this.modalUser.hide();
      this.flagUser = {
        addUser: false,
        editUser: false,
        deleteUser: false,
        import: false,
      }
      this.newUsers;
    },
    // Срабатывание сигнала создания нового пользователя
    userCreate() {
      this.checkValid = true;
      if (this.validForm) {
        this.axios.post('/user', this.currentUser).then((response) => {
          this.currentUser = {};
          this.userCancel();
          this.getUserData();
        }).catch((error) => {
          console.log('Ошибка запроса: ', error);
        });;
      }
    },
    // Срабатывание сигнала обновления даннных о пользователе
    userUpdate() {
      this.checkValid = true;
      if (this.validForm) {
        this.axios.put(`/user/${this.currentUser.id}`, this.currentUser).then((response) => {
          this.currentUser = this.users.find(item => item.id == this.currentUser.id);
          this.userCancel();
          this.getUserData();
        }).catch((error) => {
          console.log('Ошибка запроса: ', error);
        });
      }
    },
    // Срабатывание сигнала удаления пользователя
    userDelete() {
      this.axios.delete(`/user/${this.currentUser.id}`, this.currentUser).then((response) => {
        this.currentUser = {};
        this.userCancel();
        this.getUserData();
      }).catch((error) => {
        console.log('Ошибка запроса: ', error);
      });
    },
    // Выбор текущего пользователя при нажатии на строку списка
    selectUser(user) {
      if (this.currentUser != user) {
        this.currentUser = user;
      } else {
        this.currentUser = {};
      }
    },
    // Срабатывание сигнала импорта пользователей из файла
    userImport() {
      console.log(this.newUsers)
      const data = {
        'users_import': this.newUsers,
      }
      this.axios.post('/user/import', data)
        .then((response) => {
          console.log(response);
          this.users = response.data;
          this.currentUser = {};
          this.userCancel();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Отмена выбора пользователя при нажатии на Escape или клике в другой области вне списка
    unSelectUser(event) {
      if (event.type == 'keydown') {
        if (event.key == 'Escape' && !(this.flagUser.editUser || this.flagUser.deleteUser || this.flagUser.addUser)) {
          this.currentUser = {};
        }
      } else if (event.type == 'click') {
        if (this.$refs.userlist) {
          if (!(this.$refs.userlist.contains(event.target) || this.$refs.tools.contains(event.target)) &&
            !(this.flagUser.editUser || this.flagUser.deleteUser || this.flagUser.addUser)) {
            this.currentUser = {};
          }
        }
      }
    },
    // Выбор текущей страницы списка пользователей
    changePage(pageNumber) {
      this.currentPage = pageNumber;
    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalUser = new Modal('#modalUser', { backdrop: 'static' });
    // Присоединение обработчика события нажатия на клавишу и клике мышкой 
    window.addEventListener('keydown', this.unSelectUser);
    document.addEventListener('click', this.unSelectUser);
    // Запросы данных при загрузке страницы
    this.getUserData({ role: this.queryRole });
    this.getRolesData();
  },
  computed: {
    // функция пагинации списка пользователей для постраничного вывода на экран
    displayUsers() {
      this.totalPages = Math.ceil(this.foundUsers.length / this.pageSize);
      const startSlice = this.pageSize * (this.currentPage - 1);
      const endSlice = this.currentPage * this.pageSize;
      return this.foundUsers.slice(startSlice, endSlice);
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
    },
    users() {
      this.showUsersData = true;
    }
  }
}
</script>

<style scoped>
.img-btn-photo,
.img-btn-pass,
.img-btn-import,
.img-btn-edit,
.img-btn-del {
  border: none;
  width: 30px;
  height: 30px;
  cursor: pointer;
  margin-left: 5px;
}

/* .img-btn-photo {
  background: url('@/assets/img/photo-btn.png') no-repeat 50%;
  background-size: 100%;
}

.img-btn-pass {
  background: url('@/assets/img/password-btn.png') no-repeat 50%;
  background-size: 100%;
} */
.img-btn-import {
  background: url('@/assets/img/import-btn.png') no-repeat 50%;
  background-size: 100%;
}
.img-btn-edit {
  background: url('@/assets/img/edit-btn.png') no-repeat 50%;
  background-size: 100%;
}

.img-btn-del {
  background: url('@/assets/img/delete-btn.png') no-repeat 50%;
  background-size: 100%;
}

.select-user {
  background-color: rgb(161, 161, 161) !important;
}

.user-list-item {
  display: inline-block;
  margin-right: 10px;
}

.user-list-enter-active {
  transition: all 0.4s ease;
}

.user-list-enter-from {
  opacity: 0;
  transform: translateX(130px);
}
</style>