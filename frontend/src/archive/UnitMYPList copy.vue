<template>
  <div>
    <!-- Блок фильтрации юнитов MYP по подразделению и учителю -->
    <div class="row border-bottom mb-2">
      <div class="col-md-5">
        <select id="department" class="form-select me-3 mb-2" v-model="filterQueryDepartments">
          <option :value="''" selected>Все подразделения</option>
          <option v-for="(department, i) in departments" :key="i" :value="department.id">
            {{ department.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <select id="subject" class="form-select me-3 mb-2" v-model="filterQueryTeachers">
          <option :value="''" selected>Все учителя</option>
          <option v-for="(teacher, i) in filteredTeachersByDepartment" :key="i" :value="teacher.id">
            {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
          </option>
        </select>
      </div>
      <div class="col-md d-flex">
        <button type="button" class="btn btn-primary ms-auto mb-2" @click="showModalUnit">
          Cоздать MYP юнит
        </button>
      </div>
    </div>
    <!-- Модальное окно добавления юнита -->
    <modal-unit :modalTitle="modalTitle" @cancel="hideModalUnit" @create="createUnit">
      <unit-form :unit="unit" :grades="gradesMYP" :teachers="teachers" :subjects="subjects"/>
    </modal-unit>
    <!-- Блок таблицы и дополнительной фильтрации -->
    <div class="row">
      <!-- Фильтрация по предмету и году обучения -->
      <div class="col-md-2 border-end">
        <div class="d-flex flex-md-column align-items-center align-items-md-start">
          <a href="#" class="me-2" @click="filterQuerySubject = false">Все предметы</a>
          <a href="#" class="me-2" v-for="sb in subjectsUnits" :key="sb" @click="filterQuerySubject = sb">
            <span>{{ sb.name_rus }}</span>
          </a>
        </div>
        <div class="d-flex flex-md-column align-items-center align-items-md-start" v-if="yearsUnits.length > 0">
          <div class="my-3 me-2">Года обучения</div>
          <div class="me-2" v-for="year in yearsUnits" :key="year.id">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" :value="year" :id="'year-' + year.id" v-model="filterQueryYear">
              <label class="form-check-label" :for="'year-' + year.id">
                <span v-if="year.id">{{ year.year_ib }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      <!-- Таблица вывода юнитов MYP -->
      <div class="col-md flex-grow-1">
        <table class="table table-sm table-bordered mt-0">
          <thead>
            <tr class="align-middle">
              <th class="text-center" style="min-width: 10px">№</th>
              <th scope="col" class="text-center">Название</th>
              <th scope="col" class="text-center" style="width: 10%">Концепты</th>
              <th scope="col" class="text-center" style="width: 15%">Глоб. контекст</th>
              <th scope="col" class="text-center" style="width: 20%">Исследование</th>
              <th scope="col" class="text-center" style="width: 10%">Критерии оценки</th>
              <th scope="col" class="text-center" style="width: 20%">ATL</th>
            </tr>
          </thead>
          <tbody v-if="Object.keys(groupedUnits).length !== 0">
            <!-- Вывод строк таблицы сгруппированных по годам обучения юнитов -->
            <template v-for="(units, grade) in groupedUnits" :key="grade">
              <tr><td colspan="7" class="text-center bg-light fw-bold" v-if="findGrade(grade)">{{ findGrade(grade).year_ib }} ({{ findGrade(grade).year_rus }} класс)</td></tr>
              <unit-myp-item v-for="unitplan in units" :key="unitplan.id" :unitplan="unitplan" />
            </template>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="7">Юнитов не найдено</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import UnitMypItem from "@/components/UnitMYPItem";
import UnitForm from "@/components/UnitForm.vue";
import { getUnits } from "@/hooks/getUnits";
import { getSubjectsUnits } from "@/hooks/getSubjectsUnits";
import { getYearsUnits } from "@/hooks/getYearsUnits";
import { getGrades } from "@/hooks/getGrades";

import { getSubjects } from "@/hooks/getSubjects";
import { filterUnitsByTeachers } from "@/hooks/filterUnitsByTeachers";
import { filterUnitsBySubject } from "@/hooks/filterUnitsBySubject";
import { filterTeachersByDepartment } from "@/hooks/filterTeachersByDepartment";
import { filterUnitsByDepartment } from "@/hooks/filterUnitsByDepartment";
import { filterUnitsByYear } from "@/hooks/filterUnitsByYear";
import { Modal } from 'bootstrap';
import axios from 'axios';
const BASE_API_URL = 'http://localhost:8000/api/v1';

export default {
  name: 'UnitList',
  components: {
    UnitMypItem, UnitForm
  },
  props: {
    departments: {
      type: Array,
      required: true,
    },
    teachers: {
      type: Array,
      required: true,
    }
  },
  setup(props) {
    // Получение списка всех подразделений, учителей, годов обучения (MYP и DP) и базовых предметов (ООО и СОО)
    const { gradesMYP, gradesDP } = getGrades();
    const { subjects } = getSubjects('ooo', 'base');
    // Фильтрация списка учителей по выбранному подразделению
    const { filterQueryDepartments, filteredTeachersByDepartment } = filterTeachersByDepartment(teachers);
    // Получение юнитов и функции получения юнитов
    const { units, getUnitsData } = getUnits();
    // Фильтрация юнитов по выбранному подразделению
    const { filteredUnitsByDepartment } = filterUnitsByDepartment(units, filterQueryDepartments);
    // Фильтрация юнитов по выбранному учителю с учётом выбранного подразделения
    const { filterQueryTeachers, filteredUnitsByTeachers } = filterUnitsByTeachers(filteredUnitsByDepartment);
    // Получение списка предметов по существующим юнитам с учётом фильтрации по учителям и подразделениям
    const { subjectsUnits } = getSubjectsUnits(filteredUnitsByTeachers);
    // Фильрация юнитов по предметам с учётом фильтрации по учителям и подразделениям
    const { filterQuerySubject, filteredUnitsBySubject } = filterUnitsBySubject(filteredUnitsByTeachers);
    // Получение годов обучения по всем отфильтрованным юнитам
    const { yearsUnits } = getYearsUnits(filteredUnitsBySubject);
    // Фильтрация юнитов по годам обучения
    const { filterQueryYear, filteredUnitsByYear } = filterUnitsByYear(filteredUnitsBySubject);
    
    return {
      units, subjectsUnits, getUnitsData, gradesMYP, subjects, yearsUnits, filterQueryYear, filteredUnitsByYear,
      filterQueryTeachers, filteredUnitsByTeachers, filterQuerySubject, filteredUnitsBySubject, filterQueryDepartments, filteredTeachersByDepartment
    }
  },
  
  data() {
    return {
      modalUnit: {},
      unitFormVals: {},
      modalTitle: '',
      newUnitDefault: {
        authors_ids: [],
        criteria_ids: [],
      },
      unit: {},
      filteredUnits: [],
    }
  },
  methods: {
    showModalUnit() {
      this.modalTitle = 'Создание юнита';
      this.modalUnit.show();
    },
    hideModalUnit() {
      this.unit = Object.assign({}, this.newUnitDefault);
      this.modalUnit.hide();
    },
    // Валидация формы
    validationForm(form) {
      let errors = {};
      errors.order = form.querySelector("#order").value ? false : true;
      errors.title = form.querySelector("#title").value ? false : true;
      errors.authors = form.querySelector(".js-authors:checked") ? false : true;
      errors.grades = form.querySelector("#grades").value ? false : true;
      errors.subject = form.querySelector("#subject").value ? false : true;
      errors.hours = form.querySelector("#hours").value ? false : true;
      errors.criteria = form.querySelector(".js-criteria:checked") ? false : true;
      this.displayErrors(errors, form);
      for (let key in errors) {
        if (errors[key]) {
          console.log("Ошибка валидации формы");
          return true;
        }
      }
      return false;
    },
    // Вывод ошибок заполнения формы
    displayErrors(errors, form) {
      for (let key in errors) {
        if (['criteria', 'authors'].includes(key)) {
          errors[key] ? form.querySelector(`.js-${key}-label`).classList.add('error-label') : form.querySelector(`.js-${key}-label`).classList.remove('error-label');
        } else {
          errors[key] ? form.querySelector(`#${key}`).classList.add('error-input') : form.querySelector(`#${key}`).classList.remove('error-input');
          errors[key] ? form.querySelector(`label[for=${key}`).classList.add('error-label') : form.querySelector(`label[for=${key}`).classList.remove('error-label');
        } 
      }
    },
    // Создание юнита
    createUnit() {
      const config = {
        // headers: {
        //   Authorization: `Bearer ${jwt}`,
        // },
      };
      if (!this.validationForm(this.unitFormVal)) {
        this.fetchCreateUnit(this.unit, config);
      };
    },
    // Отправка POST-запроса для создания юнита
    fetchCreateUnit(requestData, config) {
      axios.post(`${BASE_API_URL}/unitplans/myp`, requestData, config)
        .then(() => {
          this.getUnitsData();
          this.unit = Object.assign({}, this.newUnitDefault);
          this.modalUnit.hide();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    findGrade(id) {
      return this.gradesMYP.find(item => item.id == id); 
    },
    findSubject(id) {
      return this.subjects.find(item => item.id == id); 
    },
  },
  computed: {
    // преобраование массива юнитов в группированный по классу объект массивов
    groupedUnits() {
      let groupedObject = this.filteredUnitsByYear.reduce((acc, obj) => {
        const property = obj.class_year.id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
  },
  mounted() {
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    this.unit = Object.assign({}, this.newUnitDefault);
    modalUnit.addEventListener('hide.bs.modal', function (event) {
      console.log("Закрытие модального окна");
    })
    this.unitFormVal = document.getElementById('unit-form');
  },
  watch: {
    filterQueryTeachers() {
      this.filterQuerySubject = '';
    },
    filterQueryDepartments() {
      this.filterQueryTeachers = '';
      this.filterQuerySubject = '';
    },
    yearsUnits() {
      this.filterQueryYear = this.yearsUnits
      console.log(this.yearsUnits)
    }
  }
}
</script>

<style scoped>
  .error-input {
    border:1px solid red;
  }
  .error-label {
    color: red;
  }
</style>