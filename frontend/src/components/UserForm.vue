<template>
  <form>
    <div class="row mt-2">
      <div class="col">
        <label for="first-name" class="form-label">Имя:</label>
        <input id="first-name" class="form-control" type="text" v-model="user.first_name" required>
      </div>
      <div class="col">
        <label for="last-name" class="form-label">Фамилия:</label>
        <input id="last-name" class="form-control" type="text" v-model="user.last_name" required>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="middle-name" class="form-label">Отчество:</label>
        <input id="middle-name" class="form-control" type="text" v-model="user.middle_name">
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="username" class="form-label">Логин:</label>
        <input id="username" class="form-control" type="text" autocomplete="off" v-model="user.username" required>
      </div>
      <div class="col-8">
        <label for="email" class="form-label">E-mail:</label>
        <input id="email" class="form-control" type="text" v-model="user.email" required>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="pass" class="form-label">Пароль:</label>
        <input id="pass" class="form-control" type="password" autocomplete="new-password" v-model="user.password"
          required>
      </div>
      <div class="col">
        <label for="pass-repeat" class="form-label">
          Повторите пароль:</label>
        <input id="pass-repeat" class="form-control" type="password" v-model="user.password_repeat"
          autocomplete="new-password" required>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="date-of-birth" class="form-label">Дата
          рождения:</label>
        <input id="date-of-birth" class="form-control" type="date" v-model="user.date_of_birth" required>
      </div>
      <div class="col">
        <label for="gender" class="form-label">Пол:</label>
        <select id="class" class="form-select" v-model="user.gender">
          <option v-for="(gn, i) in gender" :key="i" :value="gn.letter">
            {{ gn.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="border rounded p-2 mt-3">
      <h5 class="mt-2">Выберите роль: </h5>
      <div class="row mt-2">
        <div class="col" v-for="role in roles" :key="role">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" :value="role" :id="'check-' + role.id" v-model="user.role">
            <label class="form-check-label" :for="'check-' + role.id">
              {{role.name}}
            </label>
          </div>
        </div>
      </div>
      <div v-if="checkRole('Студент')">
        <div class="row mt-2">
          <div class="col">
            <label for="id-dnevnik-student" class="form-label">ID студента:</label>
            <input id="id-dnevnik-student" class="form-control" type="text" v-model="user.student.id_dnevnik">
          </div>
          <div class="col">
            <label for="class" class="form-label">Класс:</label>
            <select id="class" class="form-select" v-model="user.student.group">
              <option v-for="(gr, i) in groups" :key="i" :value="gr">
                {{ gr.class_year }}{{ gr.letter }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div v-if="checkRole('Учитель')">
        <div class="row mt-2">
          <div class="col">
            <label for="id-dnevnik-teacher" class="form-label">ID учителя:</label>
            <input id="id-dnevnik-teacher" class="form-control" type="text" v-model="user.teacher.id_dnevnik">
          </div>
          <div class="col-7">
            <label for="deparment" class="form-label">Подразделение:</label>
            <select id="deparment" class="form-select" v-model="user.teacher.department">
              <option v-for="(dp, i) in departments" :key="i" :value="dp">
                {{ dp.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true,
      default: {
        username: '',
        password: '',
        email: '',
        first_name: '',
        middle_name: '',
        last_name: '',
        date_of_birth: '',
        password_repeat: '',
        year: '',
        gender: 'O',
        role: [],
        student: {
          id_dnevnik: '',
          group: '',
        },
        teacher: {
          id_dnevnik: '',
          department: '',
        },
      }
    }
  },
  data() {
    return {
      roles: [
        { id: 1, name: 'Студент' },
        { id: 2, name: 'Учитель' },
        { id: 3, name: 'Администрация' },
      ],
      gender: [
        { name: 'Мужской', letter: 'M' },
        { name: 'Женский', letter: 'F' },
        { name: 'Не указан', letter: 'O' }],
    }
  },
  methods: {
    checkRole(role) {
      if (this.user.role) {
        const arrayRole = this.user.role.map((element) => (element.name));
        return arrayRole.includes(role);
      }
      return false;
    },
  }
}
</script>

<style scoped>

</style>