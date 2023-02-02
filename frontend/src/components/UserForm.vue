<template>
  <form>
    <div class="row mt-2">
      <div class="col">
        <label for="last-name" class="form-label">Фамилия:</label>
        <input id="last-name" class="form-control" type="text" v-model="modelValue.last_name" @input="updateFieldUnit('last_name', $event.target.value)" required>
        <small ref="last_name_alert" class="alert-text"></small>
      </div>
      <div class="col">
        <label for="first-name" class="form-label">Имя:</label>
        <input id="first-name" class="form-control" type="text" v-model="modelValue.first_name" @input="updateFieldUnit('first_name', $event.target.value)" required>
        <small ref="first_name_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="middle-name" class="form-label">Отчество:</label>
        <input id="middle-name" class="form-control" type="text" v-model="modelValue.middle_name" @input="updateFieldUnit('middle_name', $event.target.value)">
        <small ref="middle_name_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="username" class="form-label">Логин:</label>
        <input id="username" class="form-control" type="text" autocomplete="off" v-model="modelValue.username" @input="updateFieldUnit('username', $event.target.value)" required>
        <small ref="username_alert" class="alert-text"></small>
      </div>
      <div class="col-8">
        <label for="email" class="form-label">E-mail:</label>
        <input id="email" class="form-control" type="text" v-model="modelValue.email" @input="updateFieldUnit('email', $event.target.value)" required>
        <small ref="email_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2" v-if="addMode">
      <div class="col">
        <label for="pass" class="form-label">Пароль:</label>
        <input id="pass" class="form-control" type="password" autocomplete="new-password" v-model="modelValue.password" 
        @input="updateFieldUnit('password', $event.target.value)" required>
        <small ref="password_alert" class="alert-text"></small>
      </div>
      <div class="col">
        <label for="pass-repeat" class="form-label">
          Повторите пароль:</label>
        <input id="pass-repeat" class="form-control" type="password" v-model="modelValue.password_repeat" 
          @input="updateFieldUnit('password_repeat', $event.target.value)" autocomplete="new-password" required>
        <small ref="password_repeat_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md">
        <label for="date-of-birth" class="form-label">Дата рождения:</label>
        <input id="date-of-birth" class="form-control" type="date" v-model="modelValue.date_of_birth" @input="updateFieldUnit('date_of_birth', $event.target.value)" required>
      </div>
      <div class="col-md">
        <label for="gender" class="form-label">Пол:</label>
        <select id="class" class="form-select" v-model="modelValue.gender" @change="updateFieldUnit('gender', $event.target.value)">
          <option v-for="(gn, i) in gender" :key="i" :value="gn.letter">
            {{ gn.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="border rounded p-2 mt-3" v-if="modelValue.roles_ids">
      <h5 class="mt-2">Выберите роль: </h5>
      <div class="my-2" v-for="role in roles" :key="role">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" :value="role.id" :id="'check-' + role.id" v-model="modelValue.roles_ids" @change="updateFieldUnit('roles_ids', $event.target.value)">
          <label class="form-check-label" :for="'check-' + role.id">
            {{role.name}}
          </label>
        </div>
        <div v-if="role.id == 1 && this.modelValue.roles_ids.includes(1)" class="row my-2">
          <div class="col-md">
            <label for="id-dnevnik-student" class="form-label">ID студента:</label>
            <input id="id-dnevnik-student" class="form-control" type="text" v-model="modelValue.student.id_dnevnik">
          </div>
          <div class="col-md">
            <label for="class" class="form-label">Класс:</label>
            <select id="class" class="form-select" v-model="modelValue.student.group_id">
              <option :value="null">Выберите класс</option>
              <option v-for="(gr, i) in groups" :key="i" :value="gr.id">
                {{ gr.class_year }}{{ gr.letter }}
              </option>
            </select>
          </div>
        </div>
        <div v-if="role.id == 2 && this.modelValue.roles_ids.includes(2)" class="row my-2">
          <div class="col">
            <label for="id-dnevnik-student" class="form-label">ID учителя:</label>
            <input id="id-dnevnik-student" class="form-control" type="text" v-model="modelValue.teacher.id_dnevnik">
          </div>
        </div>
      </div>
      <small ref="roles_ids_alert" class="alert-text"></small>
      <small ref="student_alert" class="alert-text"></small>
    </div>
  </form>
</template>

<script>
import { toRefs } from 'vue'

export default {
  props: {
    modelValue: { type: Object },
    roles: { type: Array },
    groups: { type: Array },
    addMode: { type: Boolean },
    checkValid: { type: Boolean },
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
        student: 'Выберите группу студента',
        roles_ids: 'Выберите хотя бы одну роль пользователя',
      },
      errorField: {},
    }
  },
  methods: {
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.modelValue.first_name ? this.errorField.first_name = false : this.errorField.first_name = true;
      this.modelValue.last_name ? this.errorField.last_name = false : this.errorField.last_name = true;
      this.modelValue.username ? this.errorField.username = false : this.errorField.username = true;
      this.modelValue.email ? this.errorField.email = false : this.errorField.email = true;
      this.modelValue.roles_ids.includes(1) && this.modelValue.student.group_id ? this.errorField.student = true : this.errorField.student = false;
      this.modelValue.roles_ids.length ? this.errorField.roles_ids = false : this.errorField.roles_ids = true;
      if (this.addMode) {
        this.modelValue.password ? this.errorField.password = false : this.errorField.password = true;
        this.modelValue.password && this.modelValue.password_repeat == this.modelValue.password ? this.errorField.password_repeat = false : this.errorField.password_repeat = true;
      }
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('validForm', validate);
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
    // Обновление данных создаваемого пользователя (переменной currentUser из родительского компонента)
    updateFieldUnit(key, value) {
      this.$emit('modelValue', {...this.modelValue, [key]: value });
      this.checkFieldsValidate();
      if (this.checkValid) { this.validateForm(); }
    },
  },
  mounted() {

  },
  watch: {
    // Наблюдение за переменной со списком ролей пользователя для сброса значений связанных данный учителя и студента
    'modelValue.roles_ids': {
      handler(value) {
        if (value) {
          if (!value.includes(1)) {
            this.modelValue.student = {
              group: null,
            };
          } else if (!value.includes(2)) {
            this.modelValue.teacher = {};
          }
        }
      },
    },
    // Наблюдение за переменной-флагом необходимости валидации формы (запуск валидации при true)
    checkValid: {
      handler(value) {
        if (value) {
          this.checkFieldsValidate();
          this.validateForm();
        }
      }
    }
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
</style>