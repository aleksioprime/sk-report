<template>
  <form id="unit-form">
    <div class="row mt-2">
      <div class="col">
        <label for="title" class="form-label">Название:</label>
        <input id="title" class="form-control" type="text" v-model="unit.title">
      </div>
    </div>
    <div class="row mt-3">
      <div class="col">
        <div class="d-flex align-items-center mb-2">
          <div class="me-3 js-authors-label">Выберите авторов: </div>
          <div class="flex-grow-1"><input id="authors" class="form-control" type="text" v-model="searchAuthors" placeholder="Введите фамилию для поиска..."></div>
        </div>
        <div v-for="teacher in searchTeachers" :key="teacher.id">
          <div class="form-check">
            <input class="form-check-input js-authors" type="checkbox" :value="teacher.id" :id="'teacher-' + teacher.id" v-model="unit.authors_ids">
            <label class="form-check-label" :for="'teacher-' + teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
            </label>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <label for="grades" class="form-label">Год обучения:</label>
        <select id="grades" class="form-select" v-model="unit.class_year_id">
          <option v-for="(gr, i) in grades" :key="i" :value="gr.id">
            {{ gr.year_rus }} класс ({{ gr.year_ib }})
          </option>
        </select>
      </div>
      <div class="col">
        <label for="subject" class="form-label">Предмет:</label>
        <select id="subject" class="form-select" v-model="unit.subject_id" @change="setQuerySubject(unit.subject_id)">
          <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
            {{ sb.name_rus }}
          </option>
        </select>
      </div>
      <div class="col-2">
        <label for="hours" class="form-label">Часы:</label>
        <input id="hours" class="form-control" type="number" v-model="unit.hours">
      </div>
    </div>
    <div class="row mt-2">
      <div class="col">
        <div class="mb-2 js-criteria-label">Критерии оценки: </div>
        <div v-if="filteredCriteriaBySubject.length > 0 ">
          <div v-for="cr in filteredCriteriaBySubject" :key="cr.id">
            <div class="form-check">
              <input class="form-check-input js-criteria" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="unit.criteria_ids">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}.</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Для выбора критериев оценки укажите дисциплину</div>  
      </div>
    </div>
  </form>
</template>
  
<script>
import { filterCriteriaBySubject } from "@/hooks/unit/myp/filterCriteriaBySubject";
import { toRefs } from 'vue'

export default {
  props: {
    unit: { type: Object },
    grades: { type: Array },
    teachers: { type: Array },
    subjects: { type: Array },
    criteria: { type: Array },
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
    }
  },
  methods: {
    // Получение предметной группы выбранного предмета и запись в переменную для фильтрации критерниев
    setQuerySubject(id) {
      let subject = this.subjects.find((sb) => sb.id == id)
      this.querySubject = subject.group_ib.id;
    }
  },
  computed: {
    // фильтрация чекбоксов с учителями (searchTeachers) по значению поля ввода (searchAuthors)
    searchTeachers () {
      if (this.searchAuthors == '') {
        return this.teachers.filter(teacher => this.unit.authors_ids.includes(teacher.id))
      } 
      return this.teachers.filter(teacher => (teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.unit.authors_ids.includes(teacher.id)))
    }
  },
  mounted() {
  },
  watch: {
    // удаление выбранного предмета для фильтрации критериев оценки
    // за этим следует очищение критериев оценки в модульном окне
    unit() {
      if (!this.unit.subject_id) {
        this.querySubject = '';
      }
    }
  }
}
</script>
  
<style scoped>

</style>