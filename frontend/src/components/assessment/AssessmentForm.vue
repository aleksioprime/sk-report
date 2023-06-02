<template>
  <form>
    <!-- Поле для ввода названия работы -->
    <div class="topPage">
      <label class="form-label">Название итоговой работы</label>
      <input class="form-control" id="title" type="text" v-model="summativeWork.title">
      <small ref="title_alert" class="alert-text"></small>
    </div>
    <!-- Поля для ввода поиска и выбора учителя -->
    <div class="row mt-3">
      <div class="col">
        <div class="d-flex align-items-center mb-2">
          <div class="me-3">Выберите учителя </div>
          <div class="flex-grow-1">
            <input id="teachers" class="form-control" type="text" v-model="searchTeachers"
              placeholder="Введите фамилию для поиска...">
          </div>
        </div>
        <div v-if="!isTeacherLoading" class="list">
          <div v-for="teacher in filteredTeachers" :key="teacher.id">
            <div class="form-check">
              <input class="form-check-input" type="radio" :value="teacher.id"
                :id="'teacher-' + teacher.id" v-model="summativeWork.teacher_id">
              <label class="form-check-label" :for="'teacher-' + teacher.id">
                {{ teacher.first_name }} {{ teacher.middle_name }} {{ teacher.last_name }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Учителя загружаются. Пожалуйста, подождите</div>
      </div>
      <small ref="teacher_alert" class="alert-text"></small>
    </div>
    <!-- Выбор периода -->
    <div class="self">
      <label class="form-label">Период</label>
      <select id="period" class="form-select" v-model="summativeWork.period_id">
        <option :value="null">Выберите период</option>
        <option v-for="pr in periods" :key="pr.id" :value="pr.id">
          <span>{{ pr.number }} триместр ({{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }})</span>
        </option>
      </select>
      <small ref="period_alert" class="alert-text"></small>
    </div>
    <!-- Выбор предмета -->
    <div class="self">
      <label class="form-label">Предмет</label>
      <select id="subject" class="form-select" v-model="summativeWork.subject_id" @change="changeSubject">
        <option :value="null">Выберите предмет</option>
        <option v-for="sb in subjects" :key="sb.id" :value="sb.id">
          <span v-if="sb.group_ib">{{ sb.name_rus }} ({{ sb.group_ib.name_eng }})</span>
        </option>
      </select>
      <small ref="subject_alert" class="alert-text"></small>
    </div>
    <!-- Выбор юнита -->
    <div class="self">
      <label class="form-label">Юнит</label>
      <div v-if="summativeWork.subject_id">
        <select id="unit" class="form-select" v-model="summativeWork.unit_id" @change="changeUnit">
          <option :value="null">Выберите юнит</option>
          <option v-for="unit in unitListMYP" :key="unit.id" :value="unit.id">
            <span>{{ unit.class_year.year_rus }} класс - {{ unit.title }}</span>
          </option>
        </select>
      </div>
      <div v-else class="description">
        Выберите предмет, по которому есть созданные юниты
      </div>
      <small ref="unit_alert" class="alert-text"></small>
    </div>
    <!-- Выбор критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="criteriaMYP.length > 0 ">
          <div v-for="cr in criteriaMYP" :key="cr.id">
            <div class="form-check">
              <input name="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="summativeWork.criteria_ids">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}:</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else class="description">Для выбора критериев оценки укажите дисциплину</div>  
        <small ref="criteria_alert" class="alert-text"></small>
      </div>
    </div>
    <!-- Выбор классов и даты итоговой работы -->
    <div class="self">
        <div>Даты итоговых работ</div>
        <div v-if="summativeWork.unit_id">
          <div class="my-2 border p-2">
            <div v-if="summativeWork.groups.length">
              <div v-for="(gr, i) in summativeWork.groups" :key="gr.id" class="block-item mt-2">
                <div class="d-flex align-items-center">
                  <span v-if="findGroup(gr.group_id)">{{ findGroup(gr.group_id).class_year.year_rus }}{{ findGroup(gr.group_id).letter }} класс&nbsp;</span>
                  <span> ({{ new Date(gr.date).toLocaleDateString() }}, {{ gr.lesson }} урок)</span>
                </div>
                <div class="field-btn-wrapper">
                  <div class="icon icon-edit" @click="editWorkGroupDate(gr.id)"></div>
                  <div class="icon icon-del" @click="deleteWorkGroupDate(gr.id)"></div>
                </div>
              </div>
            </div>
            <div v-else class="my-2">
              Список пока пустой<br>
              <div class="description">Составьте список проведения итоговых работ в выбранных классах по датам.
                Для этого выберите класс, укажите дату проведения итоговой работы, введите номер урока в этот день и нажмите на '+'
              </div>
            </div>
            <div class="p-2 mt-2">
            <div class="mb-1">
              <span v-if="editDateGroup">Редактировать выбранную дату</span>
            </div>
            <div class="row">
              <div class="col-sm my-1">
                <select id="level" class="form-select" v-model="choisenWorkGroupDate.group_id">
                  <option :value="null">Класс</option>
                  <option v-for="gr in filteredGroups" :key="gr.id" :value="gr.id">
                    {{ gr.class_year.year_rus }}{{ gr.letter }} класс
                  </option>
                </select>
              </div>
              <div class="col-5 my-1">
                <input type="date" id="date" class="form-control" v-model="choisenWorkGroupDate.date">
              </div>
              <div class="col my-1 d-flex align-items-center">
                <input type="text" id="lesson" class="form-control me-2" placeholder="Урок" v-model="choisenWorkGroupDate.lesson">
                <div v-if="editDateGroup" class="d-flex">
                  <button class="icon icon-confirm ms-auto" @click="applyWorkGroupDate"></button>
                  <button class="icon icon-cancel ms-auto" @click="cancelWorkGroupDate"></button>
                </div>
                <button v-else class="icon icon-add ms-auto" @click="addWorkGroupDate" :disabled="!choisenWorkGroupDate.date || !choisenWorkGroupDate.lesson || !choisenWorkGroupDate.group_id"></button>
              </div>
            </div> 
          </div> 
          </div>    
          </div>
        <div v-else class="description">
          Выберите юнит
        </div>
        <small ref="groups_alert" class="alert-text"></small>
      </div>
   
  </form>
</template>

<script>
import { toRefs } from 'vue';
// import { getUnitsMYP, getCriteriaMYP, getGroups } from "@/hooks/assess/getSumWorkData";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getTeachers } from "@/hooks/user/useUser";
import { getUnitListMYP } from "@/hooks/unit/useUnitMYP";
import { getGroups } from "@/hooks/user/useGroup";
import { getPeriods } from "@/hooks/assess/usePeriod";

export default {
  props: {
    summativeWork: { type: Object },
    editMode: { type: Boolean },
    studyPrograms: { type: Object }
  },
  setup(props) {
    const { subjects, fetchGetSubjects } = getSubjects();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    const { unitListMYP, fetchGetUnitListMYP } = getUnitListMYP();
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { periods, currentPeriod, fetchGetPeriods } = getPeriods();

    return {
      subjects, fetchGetSubjects,
      teachers, isTeacherLoading, fetchGetTeachers,
      unitListMYP, fetchGetUnitListMYP,
      groups, isGroupLoading, fetchGetGroups,
      periods, currentPeriod, fetchGetPeriods,
    }
  },
  data() {
    return {
      criteriaMYP: [],
      searchTeachers: null,
      choisenWorkGroupDate: { group_id: null },
      errorField: {},
      textAlert: {
        title: 'Введите название итоговой работы',
        teacher: 'Выберите учителя',
        period: 'Выберите учебный период',
        subject: 'Выберите предмет',
        unit: 'Выберите юнит',
        groups: 'Создайте список проведения итоговых работ в выбранных классах по датам',
        criteria: 'Выберите критерии оценки',
      },
      editDateGroup: false,
    }
  },
  methods: {
    changeSubject(event) {
      this.fetchGetUnitListMYP({ subject: this.summativeWork.subject_id });
    },
    changeUnit(event) {
      let currentUnit = this.unitListMYP.find(item => item.id == event.target.value)
      this.fetchGetGroups({ class_year: currentUnit.class_year.id })
      this.criteriaMYP = [ ...currentUnit.criteria ];
    },
    addWorkGroupDate(event) {
      event.preventDefault();
      this.summativeWork.groups.push(this.choisenWorkGroupDate);
      this.choisenWorkGroupDate = { group_id: null };
    },
    editWorkGroupDate(id) {
      this.choisenWorkGroupDate = { ...this.summativeWork.groups.find(item => id == item.id) }
      this.editDateGroup = true;
    },
    deleteWorkGroupDate(id) {
      this.summativeWork.groups = this.summativeWork.groups.filter(item => item.id != id);
      this.choisenWorkGroupDate = { group_id: null };
    },
    applyWorkGroupDate() {
      this.summativeWork.groups = this.summativeWork.groups.map(item => {
        if (this.choisenWorkGroupDate.id == item.id) {
          return this.choisenWorkGroupDate
        }
        return item
      });
      this.editDateGroup = false;
      this.choisenWorkGroupDate = { group_id: null };
    },
    cancelWorkGroupDate() {
      this.editDateGroup = false;
      this.choisenWorkGroupDate = { group_id: null };
    },
    findGroup(id) {
      return this.groups.find(item => id == item.id)
    },
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.summativeWork.title ? this.errorField.title = false : this.errorField.title = true;
      this.summativeWork.period_id ? this.errorField.period = false : this.errorField.period = true;
      this.summativeWork.subject_id ? this.errorField.subject = false : this.errorField.subject = true;
      this.summativeWork.teacher_id ? this.errorField.teacher = false : this.errorField.teacher = true;
      this.summativeWork.unit_id ? this.errorField.unit = false : this.errorField.unit = true;
      this.summativeWork.groups.length ? this.errorField.groups = false : this.errorField.groups = true;
      this.summativeWork.criteria_ids.length ? this.errorField.criteria = false : this.errorField.criteria = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('validForm', validate);
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
  mounted() {
    this.fetchGetTeachers();
    if (this.editMode) {
      console.log('Открытие формы в режиме редатирования');
      this.fetchGetUnitListMYP({ subject: this.summativeWork.subject_id }).finally(() =>{
        const currentUnit = this.unitListMYP.find(item => item.id == this.summativeWork.unit_id);
        console.log('Текущий юнит ', currentUnit.class_year)
        this.fetchGetGroups({ class_year: currentUnit.class_year.id });
        this.criteriaMYP = [ ...currentUnit.criteria ];
      });
    }
    this.fetchGetPeriods({ study_year: this.currentStudyYear, program: 'MYP' });
    this.fetchGetSubjects({ program: 'MYP' });
    
  },
  watch: {
  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchteachers)
    filteredTeachers() {
      if (!this.searchTeachers) {
        return this.teachers.filter(teacher => this.summativeWork.teacher_id == teacher.id)
      }
      return this.teachers.filter((teacher) => {
        if (teacher) {
          return teacher.last_name.toLowerCase().includes(this.searchTeachers.toLowerCase()) || this.summativeWork.teacher_id == teacher.id
        } else {
          return this.summativeWork.teacher_id == teacher.id
        }
      })
    },
    filteredGroups() {
      if (!this.editDateGroup) {
        return this.groups.filter(item => !this.summativeWork.groups.map(gr => gr.group_id).includes(item.id))
      } else {
        return this.groups
      }
    }
  }
}
</script>

<style scoped>
.list {
  max-height: 200px;
  overflow-y: scroll;
  margin-top: 15px;
}
.topPage {
  padding-top: 0%;
}

.self {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.btn-table {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
}
.alert-text {
    color: red;
  }
  .text-table {
  vertical-align: center;
  text-align: center;
  }
</style>
