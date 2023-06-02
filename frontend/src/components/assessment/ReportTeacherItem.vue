<template>
  <div class="report-item area">
    <div class="student-header">
      <div class="student-photo">
        <img :src='report.student.user.photo ? report.student.user.photo : require("@/assets/img/student.svg")' alt="" width="50">
      </div>
      <div class="student-info">
        <div class="student-name">{{ report.student.user.last_name }} {{ report.student.user.first_name }}</div>
      </div>
    </div>
    <div class="assess-title collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-assessment-${report.id}`" role="button" aria-expanded="false" :aria-controls="`collapse-assessment-${report.id}`">
      <!-- Результаты студента за <span v-for="(asper, index) in period.assessment_periods" :key="asper.id">{{ asper.number }} {{ asper.type }}<span v-if="++index != period.assessment_periods.length">, </span></span>. -->
      Результаты студента по&nbsp;<b>Stream Report</b>
    </div>
    <div :id="`collapse-assessment-${report.id}`" class="collapse">
      <!-- <div class="student-assessment">
        <div class="assess-wrapper" v-if="report.assessment">
          <div class="assess-item">
            <div class="assess-criterion">{{ criteriaObject.criterion_a.letter }}. {{ criteriaObject.criterion_a.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" :class="{'criterion-a' : getMarkFromAssessment(report.assessment.criteria_b, asper.number)}"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.criteria_a, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-criterion">{{ criteriaObject.criterion_b.letter }}. {{ criteriaObject.criterion_b.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" :class="{'criterion-b' : getMarkFromAssessment(report.assessment.criteria_b, asper.number)}"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.criteria_b, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-criterion">{{ criteriaObject.criterion_c.letter }}. {{ criteriaObject.criterion_c.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" :class="{'criterion-c' : getMarkFromAssessment(report.assessment.criteria_c, asper.number)}"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.criteria_c, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-criterion">{{ criteriaObject.criterion_d.letter }}. {{ criteriaObject.criterion_d.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" :class="{'criterion-d' : getMarkFromAssessment(report.assessment.criteria_d, asper.number)}"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.criteria_d, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-sum">Оценка за ИР</div>
            <div class="assess-mark">
              <div class="mark" :class="{'grade' : getMarkFromAssessment(report.assessment.summ_grades, asper.number) }"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.summ_grades, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-form">Средняя текущая</div>
            <div class="assess-mark">
              <div class="mark" :class="{'grade' : getMarkFromAssessment(report.assessment.form_grades, asper.number) }"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.form_grades, asper.number) }}
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-final">Итоговая оценка</div>
            <div class="assess-mark">
              <div class="mark" :class="{'grade' : getMarkFromAssessment(report.assessment.final_grades, asper.number) }"
                v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(report.assessment.final_grades, asper.number) }}
              </div>
            </div>
          </div>
        </div>
        <button v-if="editable" class="field-btn-done" @click="autoFieldPeriodStreamReport">Выставить в итог</button>
      </div> -->
      <div class="p-2">Модуль временно отключен</div>
    </div>
    <div class="dnevnik-title collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-dnevnik-${report.id}`" role="button" aria-expanded="false" :aria-controls="`collapse-dnevnik-${report.id}`">
      Результаты студента по&nbsp;<b>Дневник.ру</b>
    </div>
    <div :id="`collapse-dnevnik-${report.id}`" class="collapse">
      <div class="dnevnik-wrapper">
        <div class="dnevnik-assessment">
          <div class="dnevnik-wrapper">
            <div class="mb-2">Итоговые оценки студента <b>{{ report.student.full_name }}</b> по предмету <b>{{ report.subject.name_rus }}</b>:</div>
            <div class="description">Внимание! Модуль работает в тестовом режиме</div>
            <div v-if="isDnevnik">
              <div v-if="isDataDnevnikLoading">
                <table class="table table-sm mt-2">
                  <thead>
                    <tr>
                      <td>Тип оценки</td>
                      <td>Номер периода</td>
                      <td>Дата окончания периода</td>
                      <td>Оценка</td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="mark in gradesDnevnik.marks" :key="mark.id_str">
                      <td>{{ mark.work_full.type }}</td>
                      <td>{{ mark.work_full.periodNumber + 1 }} {{ mark.work_full.periodType }}</td>
                      <td>{{ new Date(mark.work_full.targetDate).toLocaleDateString() }}</td>
                      <td>{{ mark.value }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="loader-wrapper">
                <span class="loader-simple"></span>
              </div>
              <!-- <button class="field-btn-done" @click="autoFieldPeriodDnevnik">Выставить в итог</button> -->
            </div>
            <div v-else>Вы не синхронизированы с Дневник.ру</div>
          </div>
        </div>
      </div>
    </div>
    <div class="student-assessment" v-if="program == 'myp'">
      <report-field-criteria id="student-assessment-myp" :report="report" @save="fetchSaveReport" :editable="editable"/>
    </div>
    <div class="student-assessment" >
      <report-field-final-grade id="student-assessment-final" :report="report" @save="fetchSaveReport" :program="program" :editable="editable"/>
    </div>
    <div class="student-report">
      <report-field-report id="student-report" :report="report" :dataField="report" :generate="true" :editable="editable" @save="fetchSaveReport"/>
    </div>
    <div class="student-events">
      <div class="events-title collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-events-${report.id}`" role="button" 
      aria-expanded="false" :aria-controls="`collapse-events-${report.id}`">Участие в мероприятиях</div>
      <report-field-blocks class="collapse" :id="`collapse-events-${report.id}`" :fieldData="report.events" :editable="editable"
      :fieldName="'events'" :defaultItem="defaultEvent" @save="fetchSaveReport">
        <!-- Слот для блоков показа записей -->
        <template v-slot:show="field">
          <div class="blocks-wrapper">
            <div><b>{{ field.data.title }}</b></div>
            <div>Тип: {{ field.data.type_name }}. Уровень: {{ field.data.level_name }}</div>
            <div>Результаты: {{ field.data.result }}</div>
          </div>
        </template>
        <template v-slot:form="item">  
          <div class="my-2">
            <input class="form-control my-1" type="text" v-model="item.data.title" placeholder="Название мероприятия">
            <div class="row">
              <div class="col-md">
                <select id="levels" class="form-select my-1" v-model="item.data.level">
                  <option :value="null">Выберите уровень</option>
                  <option v-for="(lvl, i) in levels" :key="i" :value="lvl.value">
                    {{ lvl.name }}
                  </option>
                </select>
              </div>
              <div class="col-md">
                <select id="types" class="form-select my-1" v-model="item.data.type_id">
                  <option :value="null">Выберите тип</option>
                  <option v-for="(type, i) in types" :key="i" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
            </div>
            <textarea class="form-control my-1" type="text" v-model="item.data.result" placeholder="Описание результатов"></textarea>
          </div>
        </template>
      </report-field-blocks>
    </div>
    <div class="author">Автор репорта: {{ report.author.user.last_name }} {{ report.author.user.first_name }} {{ report.author.user.middle_name }}</div>
    <div>Время редактирования: {{ new Date(report.updated).toLocaleDateString("ru-RU", {hour: 'numeric', minute: 'numeric', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</div>
  </div>
</template>
  
<script>
import { mapGetters, mapMutations } from 'vuex';
import ReportFieldReport from "@/components/assessment/ReportFieldReport.vue";
import ReportFieldCriteria from "@/components/assessment/ReportFieldCriteria.vue";
import ReportFieldFinalGrade from "@/components/assessment/ReportFieldFinalGrade.vue";
import ReportFieldBlocks from "@/components/assessment/ReportFieldBlocks.vue";

import { getFinalGradeDnevnik } from "@/hooks/assess/useReportTeacher";

export default {
  name: 'ReportTeacherItem',
  components: {
    ReportFieldReport, ReportFieldBlocks, ReportFieldCriteria, ReportFieldFinalGrade
  },
  props: {
    report: {
      type: Object,
      default: {
        group: {},
        student: {},
        assessment: {
          sum_grades: {},
          form_grades: {},
          final_grades: {},
        }
      }
    },
    criteria: {
      type: Array,
      default: []
    },
    period: { Object },
    types: { type: Array, default: [] },
    levels: { type: Array, default: [] },
    subject: { type: Object, default: null },
    group: { type: Object, default: {} },
    editable: { type: Boolean, default: false },
  },
  setup(props) {
    const { gradesDnevnik, isDataDnevnikLoading, fetchGetFinalGradeDnevnik } = getFinalGradeDnevnik();
    return {
      gradesDnevnik, isDataDnevnikLoading, fetchGetFinalGradeDnevnik
    }
  },
  data() {
    return {
      defaultEvent: {
        type_id: null,
        level: '0',
      },
    }
  },
  methods: {
    ...mapMutations(['clearDnevnikToken']),
    getMarkFromAssessment(assess, period) {
      if (assess) {
        const assessMark = assess.find(item => item.period == period)
        if (assessMark) {
          return assessMark.mark || 0
        } 
      }
      return 0
    },
    fetchSaveReport(data) {
      console.log('Сохранение репорта: ', data);
      let editReportStudents = { ...data }
      editReportStudents.author_id = this.authUser.teacher.id;
      editReportStudents.id = this.report.id || null
      this.$emit('updateReport', editReportStudents);
    },
    autoFieldPeriodStreamReport() {
      const data = {
        criterion_a: this.report.avg_assessment.criterion_a,
        criterion_b: this.report.avg_assessment.criterion_b,
        criterion_c: this.report.avg_assessment.criterion_c,
        criterion_d: this.report.avg_assessment.criterion_d,
      }
      this.fetchSaveReport(data);
    },
    autoFieldPeriodDnevnik() {

    },
    showDnevnikResults(event) {
      if (this.isDnevnik) {
        console.log('Запрос данных из Дневника.ру');
        this.fetchGetFinalGradeDnevnik({
          group_dnevnik: this.group.id_dnevnik, 
          // period_dnevnik: this.currentPeriod.id_dnevnik,
          subject_dnevnik: this.report.subject.id_dnevnik,
          student_dnevnik: this.report.student.id_dnevnik,
          user: this.authUser.id,
        }).finally(() => {
          if (!this.gradesDnevnik.isTokenValid) {
            this.clearDnevnikToken();
          }
        })
      }
    }
  },
  computed: {
    criteriaObject() {
      return {
        criterion_a: this.criteria.find(item => item.letter == 'A'),
        criterion_b: this.criteria.find(item => item.letter == 'B'),
        criterion_c: this.criteria.find(item => item.letter == 'C'),
        criterion_d: this.criteria.find(item => item.letter == 'D'),
      }
    },
    program() {
      if (this.subject.group_ib) {
        return this.subject.group_ib.program
      }
      return null
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin', 'isDnevnik']),
  },
  mounted() {
    const dnevnikCollapsible = document.getElementById(`collapse-dnevnik-${this.report.id}`)
    dnevnikCollapsible.addEventListener('show.bs.collapse', this.showDnevnikResults)
  }
}
</script>
  
<style scoped>
@import '@/assets/css/loaders.css';
.report-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
}

.report-item:hover {
  transition: 1s;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.4);
}

.student-header {
  display: flex;
}

.student-photo {
  margin-right: 10px;
}
.student-name {
  text-transform: uppercase;
  font-size: 1.5em;
  font-weight: 700;
}
.student-info {
  display: flex;
  align-items: center;
}
.assess-title {
  margin-top: 15px;
  padding: 10px;
  border-radius: 10px;
}

/* .assess-title::after {
  content: '   \25BC';
} */
.student-assessment {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  column-gap: 5px;
}

@media (max-width: 768px) {
  .student-assessment {
    flex-direction: column;
  }
}

.assess-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 350px;
  margin-bottom: 10px;
  row-gap: 2px;
}

.assess-item {
  display: flex;
  align-items: center;
  /* border: 0.5px solid var(--bs-secondary); */
  padding: 2px 10px;
  border-radius: 10px;
}
.assess-item.clicked {
  cursor: pointer;
}
.assess-item.clicked:hover {
  background: var(--my-focus);
}
.assess-criterion {
  text-transform: uppercase;
  font-weight: 700;
}

.assess-mark {
  font-weight: 700;
  margin-left: auto;
  display: flex;
  column-gap: 5px;
}
.assess-mark .mark {
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  padding: 5px 5px;
  border-radius: 5px;
  background: #e9e9e9;
}
.assess-mark .grade {
  color: #000;
  background: #fff;
  border: 1px solid #000;
}
.dnevnik-title {
  margin-top: 15px;
  padding: 10px;
  border-radius: 10px;
}
.dnevnik-wrapper {
  display: flex;
  flex-direction: column;
}
.dnevnik-item {
  display: flex;
  column-gap: 10px;
}
.student-assessment {
  margin-top: 10px;
}
.student-report {
  margin-top: 10px;
}
.dnevnik-assessment {
  padding: 10px;
}
.events-title {
  margin-top: 10px;
  border-radius: 10px;
  padding: 10px;
}
.accordion-button{
  padding: 10px;
}
.field-btn-done {
  max-width: 200px;
  align-self: flex-end;
}
.author {
  margin-top: 10px;
}
</style>