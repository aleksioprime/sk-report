<template>
  <form>
    <div class="row">
      <div class="col-md mt-2">
        <label for="last-name" class="form-label">Фамилия:</label>
        <input id="last-name" class="form-control" type="text" v-model="editedUser.last_name" required>
        <small ref="last_name_alert" class="alert-text"></small>
      </div>
      <div class="col-md mt-2">
        <label for="first-name" class="form-label">Имя:</label>
        <input id="first-name" class="form-control" type="text" v-model="editedUser.first_name" required>
        <small ref="first_name_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="middle-name" class="form-label">Отчество:</label>
        <input id="middle-name" class="form-control" type="text" v-model="editedUser.middle_name">
        <small ref="middle_name_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row">
      <div class="col-md mt-2">
        <label for="username" class="form-label">Логин:</label>
        <input id="username" class="form-control" type="text" autocomplete="off" v-model="editedUser.username" required>
        <small ref="username_alert" class="alert-text"></small>
      </div>
      <div class="col-md-8 mt-2">
        <label for="email" class="form-label">E-mail:</label>
        <input id="email" class="form-control" type="text" v-model="editedUser.email" required>
        <small ref="email_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row" v-if="addMode">
      <div class="col-md mt-2">
        <label for="pass" class="form-label">Пароль:</label>
        <input id="pass" class="form-control" type="password" autocomplete="new-password" v-model="editedUser.password" 
        @input="updateFieldUnit('password', $event.target.value)" required>
        <small ref="password_alert" class="alert-text"></small>
      </div>
      <div class="col-md mt-2">
        <label for="pass-repeat" class="form-label">
          Повторите пароль:</label>
        <input id="pass-repeat" class="form-control" type="password" v-model="editedUser.password_repeat" 
          @input="updateFieldUnit('password_repeat', $event.target.value)" autocomplete="new-password" required>
        <small ref="password_repeat_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row">
      <div class="col-sm mt-2">
        <label for="date-of-birth" class="form-label">Дата рождения:</label>
        <input id="date-of-birth" class="form-control" type="date" v-model="editedUser.date_of_birth" required>
      </div>
      <div class="col-sm mt-2">
        <label for="gender" class="form-label">Пол:</label>
        <select id="class" class="form-select" v-model="editedUser.gender">
          <option v-for="(gn, i) in gender" :key="i" :value="gn.letter">
            {{ gn.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="row my-2">
      <div class="col">
        <label for="id-dnevnik-student" class="form-label">ID системы Дневник:</label>
        <input id="id-dnevnik-student" class="form-control" type="text" v-model="editedUser.student.id_dnevnik">
        <small ref="dnevnik_alert" class="alert-text"></small>
      </div>
    </div>
  </form>
</template>

<script>
import { toRefs } from 'vue'

export default {
  props: {
    editedUser: { 
      type: Object,
      default: {
        student: {}
      }
    },
    currentYear: {
      type: Object,
      default: {}
    },
    addMode: { type: Boolean },
    validFormStudent: { type: Boolean },
  },
  setup(props) {
    return {
    }
  },
  data() {
    return {
      gender: [
        { name: 'Мужской', letter: 'M' },
        { name: 'Женский', letter: 'F' },
        { name: 'Не указан', letter: 'O' }],
      textAlert: {
        first_name: 'Введите имя пользователя',
        last_name: 'Введите фамилию пользователя',
        username: 'Введите логин',
        email: 'Введите электронную почту',
        password: 'Введите пароль',
        password_repeat: 'Повторите правильно пароль',
      },
      errorField: {},
    }
  },
  methods: {
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.editedUser.first_name ? this.errorField.first_name = false : this.errorField.first_name = true;
      this.editedUser.last_name ? this.errorField.last_name = false : this.errorField.last_name = true;
      this.editedUser.username ? this.errorField.username = false : this.errorField.username = true;
      this.editedUser.email ? this.errorField.email = false : this.errorField.email = true;
      if (this.addMode) {
        this.editedUser.password ? this.errorField.password = false : this.errorField.password = true;
        this.editedUser.password && this.editedUser.password_repeat == this.editedUser.password ? this.errorField.password_repeat = false : this.errorField.password_repeat = true;
      }
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('update:validFormStudent', validate);
      this.validateForm();
    },
    // Валидация формы - проверка ошибок полей формы и вывод их в виде текста на форму
    validateForm() {
      for (let key in this.errorField) {
        if (this.$refs[`${key}_alert`]) {
          if (this.errorField[key]) {
            this.$refs[`${key}_alert`].innerText = this.textAlert[key];
          } else {
            this.$refs[`${key}_alert`].innerText = "";
          }
        }
      }
    },
    // Обновление данных создаваемого пользователя (переменной editedUser из родительского компонента)
    updateFieldUnit(key, value) {
      this.$emit('update:editedUser', {...this.editedUser, [key]: value });
      this.checkFieldsValidate();
    },
  },
  mounted() {

  },
  watch: {
    
  }
}
</script>

<style scoped>
 .alert-text {
    color: red;
  }
  .alert-field {
    border-color: red;
  }
  .field-group {
    margin-top: 15px;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 5px;
  }
</style>