<template>
  <form id="unit-form">
    <!-- Поле для ввода названия юнита -->
    <div class="my-2">
      <label for="title" class="form-label">Название:</label>
      <input ref="title" id="title" class="form-control" type="text" v-model="editedUnit.title">
      <small ref="title_alert" class="alert-text"></small>
    </div>
    <!-- Поле для ввода поиска и выбора авторов юнита -->
    <div class="me-3 mb-2">Добавление авторов: </div>
    <div class="border p-2">
      <div class="mb-1">
        <input id="authors" class="form-control" type="text" v-model="searchAuthors"
          placeholder="Введите фамилию для поиска...">
      </div>
      <div v-for="(teacher, index) in searchTeachers.slice(0, 5)" :key="teacher.id">
        <div class="form-check">
          <input ref="teacher" class="form-check-input" type="checkbox" :value="teacher.id" :id="'teacher-' + teacher.id"
            v-model="editedUnit.authors_ids">
          <label class="form-check-label" :for="'teacher-' + teacher.id">
            {{ teacher.first_name }} {{ teacher.middle_name }} {{ teacher.last_name }}
          </label>
        </div>
        <div v-if="index == 4 && searchTeachers.length != 5">...</div>
      </div>
      <small ref="teacher_alert" class="alert-text"></small>
    </div>
    <div class="row my-2">
      <!-- Поле выбора года обучения  -->
      <div class="col-sm">
        <label for="grades" class="form-label">Год обучения:</label>
        <select ref="grade" id="grades" class="form-select" v-model="editedUnit.class_year_id">
          <option :value="null">Выберите год в MYP</option>
          <option v-for="(gr, i) in years" :key="i" :value="gr.id">
            {{ gr.year_rus }} класс ({{ gr.year_ib }})
          </option>
        </select>
        <small ref="year_alert" class="alert-text"></small>
      </div>
      <div class="col-sm-4">
        <label for="hours" class="form-label">Кол-во часов:</label>
        <input ref="hours" id="hours" class="form-control" type="number" v-model="editedUnit.hours">
        <small ref="hours_alert" class="alert-text"></small>
      </div>
    </div>
    <div class="row">
      <!-- Поле выбора предмета  -->
      <div class="col-md mt-2">
        <label for="subject" class="form-label">Учебный предмет:</label>
        <select ref="subject" id="subject" class="form-select" v-model="editedUnit.subject_id" @change="selectSubject">
          <option :value="null">Выберите предмет</option>
          <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
            {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
          </option>
        </select>
        <small ref="subject_alert" class="alert-text"></small>
      </div>
      <!-- Поле выбора уровня изучения предмета  -->
      <div class="col-md-4 mt-2">
        <label for="level" class="form-label">Уровень:</label>
        <div v-if="levels.length > 0">
          <select ref="level" id="levels" class="form-select" v-model="editedUnit.level_id">
            <option :value="null">Уровень</option>
            <option v-for="(lvl, i) in levels" :key="i" :value="lvl.id">
              {{ lvl.name_eng }}
            </option>
          </select>
        </div>
        <div v-else>Укажите дисциплину</div>
        <small ref="level_alert" class="alert-text"></small>
      </div>
    </div>
    <!-- Поле выбора критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="criteriaMYP.length > 0">
          <div v-for="cr in criteriaMYP" :key="cr.id">
            <div class="form-check">
              <input ref="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id"
                v-model="editedUnit.criteria_ids">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}:</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Для выбора критериев оценки укажите дисциплину</div>
        <small ref="criteria_alert" class="alert-text"></small>
      </div>
    </div>
  </form>
</template>
  
<script>
import { mapGetters } from 'vuex'
import { getTeachers } from "@/hooks/user/useUser";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getLevels } from "@/hooks/unit/useLevel";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";

export default {
  props: {
    editedUnit: {
      type: Object,
      default: {
        criteria: {}
      }
    },
    validFormUnit: { type: Boolean },
  },
  setup(props) {
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    const { years, fetchGetClassYears } = getClassYears();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { levels, fetchGetLevels } = getLevels();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();

    return {
      teachers, isTeacherLoading, fetchGetTeachers,
      years, fetchGetClassYears,
      subjects, fetchGetSubjects,
      levels, fetchGetLevels,
      criteriaMYP, fetchGetCriteriaMYP,
    }
  },
  data() {
    return {
      querySubjects: null,
      searchAuthors: '',
      textAlert: {
        title: 'Введите название юнита',
        teacher: 'Выберите хотя бы одного автора',
        year: 'Выберите год обучения',
        subject: 'Выберите предмет',
        level: 'Укажите уровень',
        hours: 'Введите часы',
        criteria: 'Выберите критерии оценки',
      },
      errorField: {},
    }
  },
  methods: {
    selectSubject() {
      if (this.editedUnit.subject_id) {
        this.fetchGetCriteriaMYP({ subject: this.editedUnit.subject_id })
      } else {
        this.criteriaMYP = []
      }
      this.fetchGetLevels({ subject: this.editedUnit.subject_id});
    },
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.editedUnit.title ? this.errorField.title = false : this.errorField.title = true;
      this.editedUnit.authors_ids.length ? this.errorField.teacher = false : this.errorField.teacher = true;
      this.editedUnit.class_year_id ? this.errorField.year = false : this.errorField.year = true;
      this.editedUnit.subject_id ? this.errorField.subject = false : this.errorField.subject = true;
      this.editedUnit.hours ? this.errorField.hours = false : this.errorField.hours = true;
      this.editedUnit.level_id ? this.errorField.level = false : this.errorField.level = true;
      this.editedUnit.criteria_ids.length ? this.errorField.criteria = false : this.errorField.criteria = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('update:validFormUnit', validate);
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
  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchAuthors)
    searchTeachers() {
      if (!this.searchAuthors) {
        return this.teachers.filter(teacher => this.editedUnit.authors_ids.includes(teacher.id))
      }
      return this.teachers.filter((teacher) => {
        if (teacher.last_name) {
          return teacher.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.editedUnit.authors_ids.includes(teacher.id)
        } else {
          return this.editedUnit.authors_ids.includes(teacher.id)
        }
      })
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    console.log('Форма создания юнита инициализирована!');
    this.fetchGetTeachers();
    this.fetchGetClassYears({ program: 'MYP' });
    this.fetchGetSubjects({ program: 'MYP' });
    this.authUser.teacher ? this.editedUnit.authors_ids.push(this.authUser.teacher.id) : this.editedUnit.authors_ids = [];
  },
  watch: {

  }
}
</script>
  
<style scoped>
@import '@/assets/css/unitview.css';

.alert-text {
  color: red;
}

.alert-field {
  border-color: red;
}
</style>