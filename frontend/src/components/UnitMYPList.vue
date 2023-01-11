<template>
  <div>
    <!-- Блок фильтрации юнитов MYP по подразделению и учителю -->
    <div class="row border-bottom mb-2">
      <div class="col-md-5">
        <select id="department" class="form-select me-3 mb-2" v-model="queryDepartment" @change="refreshUnitByDepartment">
          <option :value="''" selected>Все подразделения</option>
          <option v-for="(department, i) in departments" :key="i" :value="department.id">
            {{ department.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <select id="subject" class="form-select me-3 mb-2" v-model="queryTeacher" @change="getUnitsMYPData">
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
      <unit-form :unit="unit" :grades="grades" :teachers="teachers" :subjects="subjects" :criteria="criteriaMYP"/>
    </modal-unit>
    <!-- Блок таблицы и дополнительной фильтрации -->
    <div class="row">
      <!-- Фильтрация по предмету и году обучения -->
      <div class="col-md-3 border-end">
        <div class="d-flex flex-md-column align-items-center align-items-md-start">
          <a href="#" class="me-2" @click="querySubject = ''">Все предметы</a>
          <a href="#" class="me-2" v-for="sb in subjectsFromUnits" :key="sb" @click="querySubject = sb">
            <span>{{ sb.name_rus }}</span>
          </a>
        </div>
        <div class="d-flex flex-md-column align-items-center align-items-md-start" v-if="yearsFromUnits.length > 0">
          <div class="my-3 me-2">Года обучения</div>
          <div class="me-2" v-for="year in yearsFromUnits" :key="year.id">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" :value="year" :id="'year-' + year.id" v-model="queryYears">
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
// импорт библиотек
import { Modal } from 'bootstrap';
import { toRefs } from 'vue';
// импорт компонентов формы создания юнита и вывода SSO
import UnitForm from "@/components/UnitForm.vue";
import UnitMypItem from "@/components/UnitMYPItem";
// импорт функций Composition API
import { filterTeachersByDepartment } from "@/hooks/unit/myp/filterTeachersByDepartment";
import { getCriteriaMYP } from "@/hooks/unit/myp/getCriteriaMYP";
import { getGrades } from "@/hooks/unit/getGrades";
import { getSubjectsMYP } from "@/hooks/unit/myp/getSubjectsMYP";
import { getUnitsMYP } from "@/hooks/unit/myp/getUnitsMYP";
import { getSubjectsFromUnits } from "@/hooks/unit/myp/getSubjectsFromUnits";
import { getYearsFromUnits } from "@/hooks/unit/myp/getYearsFromUnits";
import { filterUnitsByYears } from "@/hooks/unit/myp/filterUnitsByYears";
import { filterUnitsBySubject } from "@/hooks/unit/myp/filterUnitsBySubject";

export default {
  name: 'UnitMYPList',
  components: {
    UnitMypItem, 
    UnitForm,
  },
  props: {
    departments: Array,
    teachers: Array,
  },
  setup(props) {
    const { teachers } = toRefs(props)
    // Фильтрация списка учителей по выбранному подразделению
    const { filteredTeachersByDepartment, queryDepartment } = filterTeachersByDepartment(teachers);
    // Получение списка критериев оценки
    const { criteriaMYP, getCriteriaData } = getCriteriaMYP();
    // Получение списка годов обучения в MYP
    const { grades, getGradesData } = getGrades();
    // Получение списка предметов в MYP
    const { subjects, getSubjectsData } = getSubjectsMYP();
    // Получение юнитов MYP и функции запроса юнитов по подразделению и учителю
    const { unitsMYP, queryTeacher, getUnitsMYPData } = getUnitsMYP(queryDepartment);
    // Получение предметов из всех юнитов 
    const { subjectsFromUnits } = getSubjectsFromUnits(unitsMYP);
    // Фильтрация юнитов по предмету
    const { querySubject, filteredUnitsBySubject } = filterUnitsBySubject(unitsMYP);
    // Получние годов обучения из отфильтрованных по предмету юнитов
    const { yearsFromUnits } = getYearsFromUnits(filteredUnitsBySubject);
    // Фильтрация юнитов по годам обучения
    const { queryYears, filteredUnitsByYears } = filterUnitsByYears(filteredUnitsBySubject);
    return {
      filteredTeachersByDepartment, queryDepartment, criteriaMYP, getCriteriaData, teachers, grades, getGradesData, subjects, getSubjectsData,
      unitsMYP, getUnitsMYPData, queryTeacher, subjectsFromUnits, yearsFromUnits, querySubject, 
      queryYears, filteredUnitsByYears
    }
  },
  
  data() {
    return {
      unit: {},
      newUnitDefault: {
        authors_ids: [],
        criteria_ids: [],
      },
      modalTitle: '',
      modalUnit: {},
    }
  },
  methods: {
    // Вызов модального окна для создания юнита
    showModalUnit() {
      this.modalTitle = 'Создание юнита';
      this.getCriteriaData();
      this.getSubjectsData('ooo', 'base');
      this.modalUnit.show();
    },
    // Закрытие модального окна для создания юнита
    hideModalUnit() {
      this.unit = Object.assign({}, this.newUnitDefault);
      this.modalUnit.hide();
    },
    // Создание юнита (отправка post запроса на сервер)
    createUnit() {
      console.log('Создание юнита');
      const url = `${this.state.base.baseAPI}/unitplans/myp`;
	    const config = this.state.base.configJWT;
      axios.post(url, this.unit, config)
        .then(() => {
          this.unit = Object.assign({}, this.newUnitDefault);
          this.modalUnit.hide();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Обновление юнитов при изменении подразделения
    refreshUnitByDepartment() {
      this.queryTeacher = '';
      this.getUnitsMYPData();
    },
    // Получение года обучения по его ID
    findGrade(id) {
      return this.grades.find(item => item.id == id); 
    },
  },
  computed: {
    // преобраование массива юнитов в группированный по классу объект массивов
    groupedUnits() {
      let groupedObject = this.filteredUnitsByYears.reduce((acc, obj) => {
        const property = obj.class_year.id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
  },
  mounted() {
    // Определение модального окна для создания юнита
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    this.unit = Object.assign({}, this.newUnitDefault);
    this.getGradesData('MYP');
  },
  watch: {
    // Для выделения всех галочек лет обучения в MYP
    yearsFromUnits() {
      this.queryYears = this.yearsFromUnits
    }
  }
}
</script>

<style scoped>

</style>