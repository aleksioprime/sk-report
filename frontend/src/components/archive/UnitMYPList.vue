<template>
  <div>
    <!-- <div class="alert alert-danger"></div> -->
    <!-- Блок фильтрации юнитов MYP по подразделению и учителю -->
    <div class="row border-bottom mb-2">
      <div class="col-md-5" v-if="isAdmin">
        <select id="department" class="form-select me-3 mb-2" v-model="queryDepartment" @change="refreshUnitByDepartment">
          <option :value="''" selected>Все подразделения</option>
          <option v-for="(department, i) in departments" :key="i" :value="department.id">
            {{ department.name }}
          </option>
        </select>
      </div>
      <div class="col-md" v-if="isAdmin">
        <select id="teacher" class="form-select me-3 mb-2" v-model="queryTeacher" @change="refreshUnitByTeacher" :disabled="Boolean(querySubject)">
          <option :value="''" selected>Все учителя</option>
          <option v-for="(teacher, i) in teachers" :key="i" :value="teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
          </option>
        </select>
      </div>
      <div v-else class="col-md d-flex align-items-center my-2">
        <span>Учитель:&nbsp;</span> 
        <span class="fw-bold" v-if="authUser">{{ authUser.last_name }} {{ authUser.first_name }} {{ authUser.middle_name }}</span>
      </div>
      <div class="col-md-3 d-flex">
        <button type="button" class="btn btn-primary ms-auto mb-2 w-100" @click="showModalUnit">
          Cоздать юнит
        </button>
      </div>
    </div>
    <!-- Модальное окно с формой добавления юнита -->
    <!-- checkValid - флаг необходимости проверки формы,  validForm - сигнал успешности проверки формы  -->
    <modal-unit :modalTitle="modalTitle" @cancel="hideModalUnit" @create="createUnit">
      <unit-myp-form v-model="unit" :grades="grades" :teachers="teachers" :subjects="subjects" :criteria="criteriaMYP" :levels="levels"
        :checkValid="checkValid" :resetValid="resetValid" @validForm="validFormResult"/>
    </modal-unit>
    <!-- Блок таблицы и дополнительной фильтрации -->
    <div class="row">
      <!-- Фильтрация по предмету и году обучения -->
      <div class="col-lg-3">
        <div class="d-flex flex-lg-column align-items-center align-items-lg-start flex-wrap">
          <div class="form-check me-2">
            <input class="form-check-input" type="radio" name="subject" :value="''" :id="'subject-x'" v-model="querySubject" @change="refreshUnitBySubject">
            <label class="form-check-label" :for="'subject-x'">
              Все предметы
            </label>
          </div>
          <div v-for="sb in subjectFilter" :key="sb.id" class="me-2">
            <div class="form-check">
              <input class="form-check-input" type="radio" name="subject" :value="sb.id" :id="'subject-' + sb.id" v-model="querySubject" @change="refreshUnitBySubject">
              <label class="form-check-label" :for="'subject-' + sb.id">
                {{ sb.name_rus }}
              </label>
            </div>
          </div>
        </div>
        <div class="d-flex flex-lg-column align-items-center align-items-lg-start" v-if="yearsFromUnits.length > 0">
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
      <div class="col-lg table-responsive p-2">
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
            <template v-for="(units, grade) in groupedUnits" :key="grade">
              <tr><td colspan="7" class="text-center bg-light fw-bold" v-if="findGrade(grade)">{{ findGrade(grade).year_ib }} ({{ findGrade(grade).year_rus }} класс)</td></tr>
              <unit-myp-item v-for="(unitplan, index) in units" :key="unitplan.id" :unitplan="unitplan" :index="index + 1" @export="exportUnit"/>
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
import { mapGetters } from 'vuex'
import { saveAs } from 'file-saver';
// импорт компонентов формы создания юнита и вывода SSO
import UnitMypForm from "@/components/UnitMYPForm.vue";
import UnitMypItem from "@/components/UnitMYPItem";
// импорт функций Composition API
import { getYearsFromUnits, filterUnitsByYears, getSubjectsFromDepartment, getSubjectsFromTeacher  } from "@/hooks/unit/filterUnitMYPData"
import { getUnitsMYP, getSubjectsMYP, getCriteriaMYP, getTeachers, getGrades, getLevels  } from "@/hooks/unit/getUnitMYPList"

export default {
  name: 'UnitMYPList',
  components: {
    UnitMypForm, 
    UnitMypItem,
  },
  props: {
    departments: Array,
  },
  setup(props) {
    const { departments } = toRefs(props)
    // Фильтрация списка учителей по выбранному подразделению
    // const { teachersFromDepartment, queryDepartment } = getTeachersFromDepartment(departments);
    const { subjectsFromDepartment, queryDepartment } =  getSubjectsFromDepartment(departments);
    const { subjectsFromTeacher } =  getSubjectsFromTeacher();
    // Получение юнитов MYP и функции запроса юнитов по подразделению и учителю
    const { unitsMYP, queryTeacher, querySubject, getUnitsMYPData} = getUnitsMYP(queryDepartment);
    // Получение списков учителей, годов обучения, предметов, уровней, критериев оценки
    const { teachers, getTeachersData } = getTeachers()    
    const { grades, getGradesData } = getGrades();
    const { subjects, getSubjectsData } = getSubjectsMYP();
    const { levels, getLevelsData } = getLevels();
    const { criteriaMYP, getCriteriaData } = getCriteriaMYP();
    // Получние годов обучения из отфильтрованных по предмету юнитов
    const { yearsFromUnits } = getYearsFromUnits(unitsMYP);
    // Фильтрация юнитов по годам обучения
    const { queryYears, filteredUnitsByYears } = filterUnitsByYears(unitsMYP);
    return {
      departments,
      // teachersFromDepartment, 
      queryDepartment, 
      subjectsFromDepartment, subjectsFromTeacher,
      unitsMYP, getUnitsMYPData, queryTeacher, querySubject,
      teachers, getTeachersData,
      grades, getGradesData, 
      subjects, getSubjectsData,
      levels, getLevelsData,
      criteriaMYP, getCriteriaData,
      yearsFromUnits, 
      queryYears, filteredUnitsByYears
    }
  },
  
  data() {
    return {
      validForm: false,
      checkValid: false,
      resetValid: false,
      unit: {
        subjects: [],
        authors_ids: [],
        criteria_ids: [],
      },
      newUnitDefault: {
        subjects: [],
        authors_ids: [],
        criteria_ids: [],
      },
      modalTitle: '',
      modalUnit: {},
    }
  },
  methods: {
    // Функция записи сигнала успещности валидации формы
    validFormResult(value) {
      this.validForm = value;
    },
    // Вызов модального окна для создания юнита
    showModalUnit() {
      this.modalTitle = 'Создание юнита';
      this.getCriteriaData();
      this.getSubjectsData('ooo', 'base');
      this.getTeachersData();
      this.getGradesData('MYP');
      this.getLevelsData();
      this.resetValid = false;
      this.authUser.teacher ? this.unit.authors_ids.push(this.authUser.teacher.id) : this.unit.authors_ids = [];
      this.modalUnit.show();
    },
    // Закрытие модального окна для создания юнита
    hideModalUnit() {
      this.resetValid = true;
      this.checkValid = false;
      this.unit = { ...this.newUnitDefault };
      this.modalUnit.hide();
    },
    // Создание юнита (отправка post запроса на сервер)
    createUnit() {
      this.checkValid = true;
      if (this.validForm) {
        let formData = { ...this.unit };
        formData.subjects = [... this.unit.subjects.map(item => {  
          return { subject_id: item.subject.id, level_id: item.level.id }
        })]
        this.axios.post('/unitplans/myp', formData).then((response) => {
          this.hideModalUnit();
          this.$store.dispatch('getUserData');
          this.getUnitsMYPData();
        });
      }
    },
    // Экспорт юнита
    exportUnit(unit) {
      console.log(unit)
      // const data = { 'unit': id };
      // this.axios.post('/unitplans/export', data).then((response) => console.log(response));
      const config = {
        responseType: 'blob',
        params: {
          unit: unit.id,
        }
      }
      this.axios.get('/unitplans/myp/export', config).then((response) => {
        console.log(response);
        saveAs(response.data, `${unit.title.replace(/ /g,"_")}.docx`);
      });
    },
    // Обновление юнитов при выборе подразделения
    refreshUnitByDepartment() {
      this.queryTeacher = '';
      this.querySubject = '';
      this.getUnitsMYPData();
    },
    // Обновление юнитов при выборе учителя
    refreshUnitByTeacher() {
      this.querySubject = '';
      this.getUnitsMYPData();
    },
    // Обновление юнитов при выборе предмета
    refreshUnitBySubject() {
      this.getUnitsMYPData();
    },
    // Получение данных о годе обучения по его ID
    findGrade(id) {
      return this.yearsFromUnits.find(item => item.id == id); 
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
    subjectFilter() {
      if (this.isAdmin) {
        return this.subjectsFromDepartment
      } else {
        return this.subjectsFromTeacher(this.authUser)
      }
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    // Определение модального окна для создания юнита
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    // Автоматическая загрузка юнитов и учителей при монтировании страницы
    // Если пользователь не администратор, то фильтра по подразделению и учителя нет, 
    // а в таблицу подгруджаются юниты текущего учителя
    if (this.isAdmin) {
      this.getTeachersData();
    } else {
      this.authUser.teacher ? this.queryTeacher = this.authUser.teacher.id : this.queryTeacher = '';
    }
    this.getUnitsMYPData();
  },
  watch: {
    // Автовыделение всех лет обучения в MYP в меню фильтра
    yearsFromUnits() {
      this.queryYears = this.yearsFromUnits
    },
    // Сигнал успешности загрузки юнитов на странице
    unitsMYP() {
      this.$emit('showMYPData', true);
    }
  }
}
</script>

<style scoped>
</style>