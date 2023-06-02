<template>
  <form id="unit-form">
    <!-- Вывод информации о междисциплинарности юнита -->
    <div class="my-2">
      <span v-if="checkInterdisciplinary" class="badge rounded-pill text-bg-primary">Междисциплинарный</span>
    </div>
    <!-- Поле для ввода названия юнита -->
    <div class="my-2">
      <label for="title" class="form-label">Название:</label>
      <input ref="title" id="title" class="form-control" type="text" v-model="modelValue.title" @input="updateFieldUnit('title', $event.target.value)">
      <small ref="title_alert" class="alert-text"></small>
    </div>
    <!-- Поле для ввода поиска и выбора авторов юнита -->
    <div class="row mt-3">
      <div class="col">
        <div class="d-flex align-items-center mb-2">
          <div class="me-3">Выберите авторов: </div>
          <div class="flex-grow-1"><input id="authors" class="form-control" type="text" v-model="searchAuthors" placeholder="Введите фамилию для поиска..."></div>
        </div>
        <div v-for="teacher in searchTeachers" :key="teacher.id">
          <div class="form-check">
            <input ref="teacher" class="form-check-input" type="checkbox" :value="teacher.id" :id="'teacher-' + teacher.id" v-model="modelValue.authors_ids" @change="updateFieldUnit('authors_ids', $event.target.value)">
            <label class="form-check-label" :for="'teacher-' + teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
            </label>
          </div>
        </div>
      </div>
      <small ref="teacher_alert" class="alert-text"></small>
    </div>
    <!-- Поля для выбора года обучения и ввода количества часов нагрузки  -->
    <div class="row mt-2">
      <div class="col-md">
        <label for="grades" class="form-label">Год обучения:</label>
        <select ref="grade" id="grades" class="form-select" v-model="modelValue.class_year_id" @change="updateFieldUnit('class_year_id', $event.target.value)">
          <option v-for="(gr, i) in grades" :key="i" :value="gr.id">
            {{ gr.year_rus }} класс ({{ gr.year_ib }})
          </option>
        </select>
        <small ref="grade_alert" class="alert-text"></small>
      </div>
      <div class="col-md-3">
        <label for="hours" class="form-label">Часы:</label>
        <input ref="hours" id="hours" class="form-control" type="number" v-model="modelValue.hours" @input="updateFieldUnit('hours', $event.target.value)">
        <small ref="hours_alert" class="alert-text"></small>
      </div>
    </div>
    <!-- Форма добавления предметов в список -->
    <div class="my-2">
      <div class="mb-2">Предметы:</div>
      <div class="unit-field-description">Чтобы добавить предмет, выберите его в выпадающем спискае и укажите его уровень, а затем нажмите на +</div>
      <div class="row">
        <div class="col-sm">
          <select id="level" class="form-select" v-model="choisenSL.subject">
            <option :value="null">Выберите предмет</option>
            <option v-for="sb in subjects" :key="sb.id" :value="sb">
              {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
            </option>
          </select>
        </div>
        <div class="col-sm-4">
          <select id="level" class="form-select" v-model="choisenSL.level" :disabled="choisenSL.subject == null">
            <option :value="null">Уровень</option>
            <option v-for="lv in filteredLevels" :key="lv.id" :value="lv">
              <div>{{ lv.name_eng }}</div>
            </option>
          </select>
        </div>
        <div class="col-sm-1 d-flex align-items-center me-3">
          <button class="img-btn-add ms-auto" @click="addSubjectLevel" :disabled="choisenSL.subject == null || choisenSL.level == null"></button>
        </div>
      </div>
      <div class="my-2">
        <table class="table border mb-0" v-if="modelValue.subjects.length">
          <tr><td class="p-2">Выбранные предметы:</td></tr>
          <tr v-for="(sb, i) in modelValue.subjects" :key="i">
            <td class="p-2"><b>{{ sb.subject.name_rus }}</b> ({{ sb.subject.group_ib.name_eng }})</td>
            <td>{{ sb.level.name_eng }}</td>
            <td>
              <button class="img-btn-del my-1" @click="deleteSubjectLevel(i)"></button>
            </td>
          </tr>
        </table>
      </div>
      <small ref="subjects_alert" class="alert-text"></small>
    </div>
    <!-- Поле выбора критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="filteredCriteriaBySubject.length > 0 ">
          <div v-for="cr in filteredCriteriaBySubject" :key="cr.id">
            <div class="form-check">
              <input ref="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="modelValue.criteria_ids" @change="updateFieldUnit('criteria_ids', $event.target.value)">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <span v-if="checkInterdisciplinary"><b>{{ cr.subject_group.name_eng }} - </b></span><b>{{ cr.letter }}:</b> {{ cr.name_eng }}
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
import { filterCriteriaBySubject } from "@/hooks/unit/filterUnitMYPData";
import { toRefs } from 'vue'

export default {
  props: {
    modelValue: { type: Object },
    grades: { type: Array },
    teachers: { type: Array },
    subjects: { type: Array },
    levels: { type: Array },
    criteria: { type: Array },
    checkValid: { type: Boolean },
    resetValid: { type: Boolean },
  },
  setup(props) {
    const { criteria } = toRefs(props);
    const { filteredCriteriaBySubject, querySubjects} = filterCriteriaBySubject(criteria);
    return {
      filteredCriteriaBySubject, querySubjects
    }
  },
  data() {
    return {
      searchAuthors: '',
      errorField: {},
      choisenSL: { subject: null, level: null },
      textAlert: {
        title: 'Введите название юнита',
        teacher: 'Выберите хотя бы одного автора',
        grade: 'Выберите год обучения',
        subjects: 'Добавьте предметы',
        hours: 'Введите часы',
        criteria: 'Выберите критерии оценки',
      },
      extraFields: ['criteria', 'teacher', 'subjects'],
    }
  },
  methods: {
    // Добавление предмета и его уровня в modelValue.subjects, изменение условия для фильтрации критериев
    addSubjectLevel(event) {
      event.preventDefault();
      this.modelValue.subjects.push(this.choisenSL);
      this.choisenSL = { subject: null, level: null };
      this.setQuerySubjects(this.modelValue.subjects);
    },
    // Удаление конкретного предмета и его уровня из modelValue.subjects, изменение условия для фильтрации критериев
    deleteSubjectLevel(i) {
      this.modelValue.subjects.splice(i, 1); 
      this.setQuerySubjects(this.modelValue.subjects);
    },
    // Изменение условия фильтрации критериев и обновление modelValue.subjects
    setQuerySubjects(subjects) {
      this.querySubjects = subjects.map(item => item.subject.group_ib.id);
      this.updateFieldUnit('subjects', subjects);
    },
    // Сброс информации о валидации формы
    resetValidForm() {
      for (let key in this.textAlert) {
        this.$refs[`${key}_alert`].innerText = "";
        if (!this.extraFields.includes(key)) { this.$refs[key].classList.remove('alert-field') };
      }
      this.searchAuthors = '';
    },
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.modelValue.title ? this.errorField.title = false : this.errorField.title = true;
      this.modelValue.authors_ids.length ? this.errorField.teacher = false : this.errorField.teacher = true;
      this.modelValue.class_year_id ? this.errorField.grade = false : this.errorField.grade = true;
      this.modelValue.subjects.length ? this.errorField.subjects = false : this.errorField.subjects = true;
      this.modelValue.hours ? this.errorField.hours = false : this.errorField.hours = true;
      this.modelValue.criteria_ids.length ? this.errorField.criteria = false : this.errorField.criteria = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('validForm', validate);
    },
    // Валидация формы - проверка введённых в форму данных 
    validateForm() {
      for (let key in this.errorField) {
        if (this.$refs[`${key}_alert`]) {
          if (this.errorField[key]) {
            if (!this.extraFields.includes(key)) { this.$refs[key].classList.add('alert-field') };
            this.$refs[`${key}_alert`].innerText = this.textAlert[key];
          } else {
            if (!this.extraFields.includes(key)) { this.$refs[key].classList.remove('alert-field') };
            this.$refs[`${key}_alert`].innerText = "";
          }
        }
      }
    },
    // Обновление данных создаваемого юнита (переменной unit из родительского)
    updateFieldUnit(key, value) {
      this.$emit('modelValue', {...this.modelValue, [key]: value });
      this.checkFieldsValidate();
      if (this.checkValid) { this.validateForm() }
    },

  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchAuthors)
    searchTeachers() {
      if (this.searchAuthors == '') {
        return this.teachers.filter(teacher => this.modelValue.authors_ids.includes(teacher.id))
      } 
      return this.teachers.filter((teacher) => {
        if (teacher.user) {
          return teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.modelValue.authors_ids.includes(teacher.id)
        } else {
          return this.modelValue.authors_ids.includes(teacher.id)
        }
      })
    },
    // Переменная с меткой междисциплинарности создаваемого юнита
    checkInterdisciplinary() {
      return this.modelValue.subjects.length > 1;
    },
    // Переменная с данными отфильтрованных уровней по выбранному предмету
    filteredLevels() {
      let levels = []
      if (this.choisenSL.subject) {
        levels = [...this.levels.filter(item => item.subject_groups.includes(this.choisenSL.subject.group_ib.id))]
        if (this.modelValue.class_year_id == 5 || this.modelValue.class_year_id == 6) {
          this.choisenSL.level = levels[0]
        } else if (this.modelValue.class_year_id == 7 || this.modelValue.class_year_id == 8) {
          this.choisenSL.level = levels[1]
        } else {
          this.choisenSL.level = levels[2]
        }
      } 
      return levels
    },
  },
  mounted() {
  },
  watch: {
    // Наблюдение за свойством subjects переменной создаваемого юнита и 
    // обнуление фильтра критериев оценки при отсутствии выбранных предметов
    modelValue: {
      handler(subjects) {
        if (subjects.length) {
          this.querySubjects = [];
        }
      },
      deep: true
    },
    // Наблюдение за переменной-флагом необходимости валидации формы (запуск валидации при true)
    checkValid: {
      handler(value) {
        if (value) {
          this.checkFieldsValidate();
          this.validateForm();
        }
      }
    },
    // Наблюдение за переменной-флагом необходимости сброса валидации формы (сброс валидации при true)
    resetValid: {
      handler(value) {
        if (value) {
          this.resetValidForm();
        }
      }
    }
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