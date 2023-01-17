<template>
  <form id="unit-form">
    <div class="my-2">
      <label for="title" class="form-label">Название:</label>
      <input ref="title" id="title" class="form-control" type="text" v-model="modelValue.title" @input="updateFieldUnit('title', $event.target.value)">
      <small ref="titleAlert" class="alert-text"></small>
    </div>
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
      <small ref="teacherAlert" class="alert-text"></small>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="grades" class="form-label">Год обучения:</label>
        <select ref="grade" id="grades" class="form-select" v-model="modelValue.class_year_id" @change="updateFieldUnit('class_year_id', $event.target.value)">
          <option v-for="(gr, i) in grades" :key="i" :value="gr.id">
            {{ gr.year_rus }} класс ({{ gr.year_ib }})
          </option>
        </select>
        <small ref="gradeAlert" class="alert-text"></small>
      </div>
      <div class="col">
        <label for="subject" class="form-label">Предмет:</label>
        <select ref="subject" id="subject" class="form-select" v-model="modelValue.subject_id" @change="setQuerySubject(modelValue.subject_id)">
          <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
            {{ sb.name_rus }}
          </option>
        </select>
        <small ref="subjectAlert" class="alert-text"></small>
      </div>
      <div class="col-2">
        <label for="hours" class="form-label">Часы:</label>
        <input ref="hours" id="hours" class="form-control" type="number" v-model="modelValue.hours" @input="updateFieldUnit('hours', $event.target.value)">
        <small ref="hoursAlert" class="alert-text"></small>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="filteredCriteriaBySubject.length > 0 ">
          <div v-for="cr in filteredCriteriaBySubject" :key="cr.id">
            <div class="form-check">
              <input ref="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="modelValue.criteria_ids" @change="updateFieldUnit('criteria_ids', $event.target.value)">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}.</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Для выбора критериев оценки укажите дисциплину</div>  
        <small ref="criteriaAlert" class="alert-text"></small>
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
    criteria: { type: Array },
    checkValid: { type: Boolean },
    resetValid: { type: Boolean },
    showValid: { type: Boolean },
  },
  setup(props) {
    const { criteria } = toRefs(props)
    const { filteredCriteriaBySubject, querySubject} = filterCriteriaBySubject(criteria);
    return {
      filteredCriteriaBySubject, querySubject
    }
  },
  data() {
    return {
      searchAuthors: '',
      errorField: {},
      textAlert: {
        title: 'Введите название юнита',
        teacher: 'Выберите хотя бы одного автора',
        grade: 'Выберите год обучения',
        subject: 'Выберите предмет',
        hours: 'Введите часы',
        criteria: 'Выберите критерии оценки',
      },
      invisibleFields: ['criteria', 'teacher'],
    }
  },
  methods: {
    // Получение предметной группы выбранного предмета и запись в переменную для фильтрации критерниев
    setQuerySubject(id) {
      let subject = this.subjects.find((sb) => sb.id == id);
      this.querySubject = subject.group_ib.id;
      this.updateFieldUnit('class_year_id', this.querySubject);
    },
    resetValidForm() {
      for (let key in this.textAlert) {
        this.$refs[`${key}Alert`].innerText = "";
        if (!this.invisibleFields.includes(key)) { this.$refs[key].classList.remove('alert-field') };
      }
      this.searchAuthors = '';
    },
    validateForm() {
      this.$refs.title.value ? this.errorField.title = false : this.errorField.title = true;
      this.$refs.teacher && this.$refs.teacher.find(item => item.checked) ? this.errorField.teacher = false : this.errorField.teacher = true;
      this.$refs.grade.value ? this.errorField.grade = false : this.errorField.grade = true;
      this.$refs.subject.value ? this.errorField.subject = false : this.errorField.subject = true;
      this.$refs.hours.value ? this.errorField.hours = false : this.errorField.hours = true;
      this.$refs.criteria && this.$refs.criteria.find(item => item.checked) ? this.errorField.criteria = false : this.errorField.criteria = true;
      let checkBool = true
      for (let key in this.errorField) {
        if (this.showValid) { this.showErrorFields(key) }
        if (this.errorField[key]) { checkBool = false }
      }
      if (checkBool) { 
        console.log('Валидация прошла успешно');
        this.$emit('validForm', true);
       }
    },
    showErrorFields(field) {
      if (!this.errorField[field]) {
        this.$refs[`${field}Alert`].innerText = "";
        if (!this.invisibleFields.includes(field)) { this.$refs[field].classList.remove('alert-field') };
      } else {
        this.$refs[`${field}Alert`].innerText = this.textAlert[field];
        if (!this.invisibleFields.includes(field)) { this.$refs[field].classList.add('alert-field') };
      }
    },
    updateFieldUnit(key, value) {
      this.$emit('modelValue', {...this.modelValue, [key]: value });
      if (this.checkValid) { this.validateForm() }
    },

  },
  computed: {
    // фильтрация чекбоксов с учителями (searchTeachers) по значению поля ввода (searchAuthors)
    searchTeachers() {
      if (this.searchAuthors == '') {
        return this.teachers.filter(teacher => this.modelValue.authors_ids.includes(teacher.id))
      } 
      return this.teachers.filter(teacher => (teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.modelValue.authors_ids.includes(teacher.id)))
    },
  },
  mounted() {
  },
  watch: {
    // удаление выбранного предмета для фильтрации критериев оценки
    // за этим следует очищение критериев оценки в модульном окне
    modelValue() {
      if (!this.modelValue.subject_id) {
        this.querySubject = '';
      }
    },
    checkValid() {
      if (this.checkValid) { this.validateForm() }
    },
    resetValid() {
      if (this.resetValid) { this.resetValidForm() }
    },
    showValid() {
      if (this.showValid) { this.validateForm() }
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