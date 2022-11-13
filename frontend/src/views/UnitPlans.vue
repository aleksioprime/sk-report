<template>
  <div>
    <h1 class="mb-2">Планы учебных модулей</h1>
    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="pills-myp-tab" data-bs-toggle="pill" data-bs-target="#pills-myp" type="button" role="tab" aria-controls="pills-myp" aria-selected="true">MYP</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="pills-dp-tab" data-bs-toggle="pill" data-bs-target="#pills-dp" type="button" role="tab" aria-controls="pills-dp" aria-selected="false">DP</button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <div class="tab-pane fade show active" id="pills-myp" role="tabpanel" aria-labelledby="pills-myp-tab">
        <div class="tools d-flex align-items-center border-bottom mb-3">
          <select id="department" class="form-select me-3 department" v-model="filterQueryDepartments">
            <option :value="''" selected>Все подразделения</option>
            <option v-for="(department, i) in departments" :key="i" :value="department.id">
              {{ department.name }}
            </option>
          </select>
          <select id="subject" class="form-select me-3 subject" v-model="filterQueryTeachers">
            <option :value="''" selected>Все учителя</option>
            <option v-for="(teacher, i) in filteredTeachersByDepartment" :key="i" :value="teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
            </option>
          </select>
          <button type="button" class="btn btn-primary ms-auto my-3" @click="showModalUnit">
            Cоздать MYP юнит
          </button>
        </div>
        <modal-unit :modalTitle="modalTitle" @cancel="hideModalUnit" @create="createUnit">
          <unit-form :unit="unit" :grades="grades" :teachers="teachers" :subjects="subjects"/>
        </modal-unit>
        <div class="sso-myp d-flex align-items-start">
          <div class="sso-subjects px-3 border-end">
            <a href="#" @click="filterQuerySubject = false">Все предметы</a><br>
            <a href="#" v-for="sb in subjectsUnits" :key="sb" @click="filterQuerySubject = sb">
              <span v-if="findSubject(sb)">{{ findSubject(sb).name_rus }}</span><br>
            </a>
            <div v-if="yearsUnits.length > 0">
              <div class="my-3">Года обучения</div>
              <div v-for="year in yearsUnits" :key="year">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" :value="year" :id="'year-' + year" v-model="filterQueryYear">
                  <label class="form-check-label" :for="'year-' + year">
                    {{ findGrade(year).year_ib }}
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="sso-table px-3 flex-grow-1">
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
                <template v-for="(units, grade) in groupedUnits">
                  <tr><td colspan="7" class="text-center bg-light fw-bold" v-if="findGrade(grade)">{{ findGrade(grade).year_ib }} ({{ findGrade(grade).year_rus }} класс)</td></tr>
                  <unit-item v-for="unitplan in units" :key="unitplan.id" :unitplan="unitplan" />
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
      <div class="tab-pane fade" id="pills-dp" role="tabpanel" aria-labelledby="pills-dp-tab">
        Этот раздел пока в разработке
      </div>
    </div>
  </div>
</template>

<script>
import UnitItem from "@/components/UnitItem";
import UnitForm from "@/components/UnitForm.vue";
import { getUnits } from "@/hooks/getUnits";
import { getSubjectsUnits } from "@/hooks/getSubjectsUnits";
import { getYearsUnits } from "@/hooks/getYearsUnits";
import { getGrades } from "@/hooks/getGrades";
import { getDepartments } from "@/hooks/getDepartments";
import { getTeachers } from "@/hooks/getTeachers";
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
  name: 'UnitPlans',
  components: {
    UnitItem, UnitForm
  },
  setup(props) {
    const { departments } = getDepartments();
    const { teachers } = getTeachers();
    const { filterQueryDepartments, filteredTeachersByDepartment } = filterTeachersByDepartment(teachers);
    const { units, getUnitsData } = getUnits();
    const { filteredUnitsByDepartment } = filterUnitsByDepartment(units, filterQueryDepartments);
    const { filterQueryTeachers, filteredUnitsByTeachers } = filterUnitsByTeachers(filteredUnitsByDepartment, filterQueryDepartments);
    const { subjectsUnits } = getSubjectsUnits(filteredUnitsByTeachers, filterQueryDepartments);
    const { filterQuerySubject, filteredUnitsBySubject } = filterUnitsBySubject(filteredUnitsByTeachers);
    const { yearsUnits } = getYearsUnits(filteredUnitsBySubject);
    const { filterQueryYear, filteredUnitsByYear } = filterUnitsByYear(filteredUnitsBySubject);
    const { grades } = getGrades('MYP');
    const { subjects } = getSubjects('ooo', 'base');
    return {
      units, subjectsUnits, getUnitsData, grades, departments, teachers, subjects, yearsUnits, filterQueryYear, filteredUnitsByYear,
      filterQueryTeachers, filteredUnitsByTeachers, filterQuerySubject, filteredUnitsBySubject, filterQueryDepartments, filteredTeachersByDepartment
    }
  },
  data() {
    return {
      modalUnit: {},
      unitForms: {},
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
      if (!this.validationForm(this.unitForm)) {
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
      return this.grades.find(item => item.id == id); 
    },
    findSubject(id) {
      return this.subjects.find(item => item.id == id); 
    },
    // filterUnits(id) {
    //   this.filteredUnits = this.filteredUnitsByTeachers.filter(unit => unit.subject.id === id);
    //   console.log(id)
    // },
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
    this.unitForm = document.getElementById('unit-form');
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
  .sso-subjects {
    width: 160px;
  }
  .sso-table {
    width: 100%;
  }
  .department {
    max-width: 320px;
  }
  .subject {
    max-width: 250px;
  }
</style>