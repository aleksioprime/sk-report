<template>
  <div class="report-item">
    <div class="student-header">
      <div class="student-photo">
        <img :src='student.user.photo ? student.photo : require("@/assets/img/student.svg")' alt="" width="50">
      </div>
      <div class="student-info">
        <div class="student-name">{{ student.user.last_name }} {{ student.user.first_name }}</div>
      </div>
      <div class="ms-auto"><div class="icon icon-export-doc" @click="exportToPDF"></div></div>
    </div>
    <div class="student-report">
      <report-field-report id="student-report" :student="student" :dataField="student.mentor_report" @save="fetchSaveReport" :editable="editable"/>
    </div>
    <div class="student-events">
      <div class="events-title collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-events-${student.id}`" role="button" 
      aria-expanded="false" :aria-controls="`collapse-events-${student.id}`">Участие в мероприятиях</div>
      <div class="events-wrapper collapse" :id="`collapse-events-${student.id}`">
        <div class="events-teacher" v-if="student.events.length">
          <div class="events-teacher-title">Мероприятия от учителей-предметников и психолога</div>
          <div v-for="event in student.events" :key="event.id" class="event-item">
            <div>{{ event.title }} ({{ event.type_name }}, {{ event.level_name }})</div>
            <div>Результаты: {{ event.result }}</div>
            <div v-if="event.teacher_report && event.teacher_report.author">Учитель: {{ event.teacher_report.author.user.last_name }} {{ event.teacher_report.author.user.first_name }} {{ event.teacher_report.author.user.middle_name }} ({{ event.teacher_report.subject.name_rus }})</div>
            <div v-if="event.psycho_report && event.psycho_report.author">Психолог: {{ event.psycho_report.author.user.last_name }} {{ event.psycho_report.author.user.first_name }} {{ event.psycho_report.author.user.middle_name }}</div>
          </div>
        </div>
        <div v-else class="events-no">
          Данных о мероприятиях от учителей-предметников и психолога пока нет
        </div>
        <report-field-blocks :fieldData="student.mentor_report.events" :fieldName="'events'" :defaultItem="defaultEvent" @save="fetchSaveReport"  v-if="student.mentor_report.text" :editable="editable">
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
    </div>
    <div class="subject-reports">
      <div class="subject-reports-title">Репорт психолога</div>
      <div v-if="student.psycho_report.text">
        <div class="subject-report">
          <div v-html="student.psycho_report.text"></div>
        </div>
        <div v-if="student.psycho_report.author">{{ student.psycho_report.author.user.last_name }} {{ student.psycho_report.author.user.first_name }} {{ student.psycho_report.author.user.middle_name }}</div>
        <div v-if="student.psycho_report.updated">Время редактирования: {{ new Date(student.psycho_report.updated).toLocaleDateString("ru-RU", {hour: 'numeric', minute: 'numeric', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</div>
      </div>
      <div v-else>Психолог пока не написал репорт</div>
      <div class="subject-reports-title">Репорты учителей-предметников</div>
      <div class="accordion" id="accordionPanelsSubject" v-if="student.subject_reports.length">
        <div class="subject-item accordion-item" v-for="subject in student.subject_reports" :key="subject.id">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="`#panels-subject-${subject.id}`" aria-expanded="true" :aria-controls="`panels-subject-${subject.id}`">
              <div class="subject-title"><h4>{{ subject.subject_name }}</h4></div>
            </button>
          </h2>
          <div :id="`panels-subject-${subject.id}`" class="accordion-collapse collapse">
            <div class="accordion-body">
              <div v-if="subject.text">
              <div class="subject-criteria" v-if="program == 'myp'">
                <div class="criteria-wrapper mb-3">
                  <div class="criteria-item" v-for="cr in subject.criteria" :key="cr.id">
                    <div class="criterion">{{ cr.criterion.letter }}. {{ cr.criterion.name_eng }}</div>
                    <div class="criteria-value">{{ cr.mark }}</div>
                  </div>
                </div>
                <div class="criteria-wrapper">
                  <div class="criteria-item">
                    <div class="criterion">Сумма баллов: </div>
                    <div class="criteria-value">{{ subject.criterion_summ || '-' }} / {{ subject.criterion_count * 8 || '-' }}</div>
                  </div>
                  <div class="criteria-item">
                    <div class="criterion">Оценка РФ: </div>
                    <div class="criteria-value">{{ subject.criterion_rus }}</div>
                  </div>
                </div>
              </div>
              <div class="subject-criteria  mt-2">
                <div class="grade-item">
                  <div class="grade-title">Итоговая оценка РФ: </div>
                  <div class="grade-value">{{ subject.final_grade }}</div>
                </div>
                <div class="grade-item" v-if="program == 'dp'">
                  <div class="grade-title">Итоговая оценка IB: </div>
                  <div class="grade-value">{{ subject.final_grade_ib }}</div>
                </div>
              </div>
              <div class="subject-report">
                <div v-html="subject.text"></div>
              </div>
              <div class="teacher-name">{{ subject.author.full_name }}</div>
              <div>Время редактирования: {{ new Date(subject.updated).toLocaleDateString("ru-RU", {hour: 'numeric', minute: 'numeric', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</div>
              </div>
              <div v-else>Нет данных</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>Учителя пока не написали репорты</div>
    </div>
  </div>
</template>
  
<script>
import { mapGetters } from 'vuex';
import { saveAs } from 'file-saver';
import ReportFieldReport from "@/components/assessment/ReportFieldReport.vue";
import ReportFieldBlocks from "@/components/assessment/ReportFieldBlocks.vue";

export default {
  name: 'ReportMentorItem',
  components: {
    ReportFieldReport, ReportFieldBlocks
  },
  props: {
    student: {
      type: Object,
      default: {
        group: {},
        mentor_report: {},
        user: {},
      }
    },
    period: { Object },
    types: { type: Array, default: [] },
    levels: { type: Array, default: [] },
    editable: { type: Boolean, default: false },
    program: { type: String }
  },

  data() {
    return {
      defaultEvent: {
        type_id: null,
        level: '0',
      }
    }
  },
  methods: {
    fetchSaveReport(data) {
      console.log('Сохранение репорта: ', data);
      let editReportStudents = { ...data }
      editReportStudents.student_id = this.student.id;
      editReportStudents.author_id = this.authUser.teacher.id;
      editReportStudents.id = this.student.mentor_report.id || null
      this.$emit('updateReport', editReportStudents);
    },
    fetchSaveEvent(data) {
      console.log('Сохранение мероприятия: ', data);
    },
    resolveBlob(response) {
      const headerval = response.headers['content-disposition'];
      if (headerval != null) {
        let filename = headerval.split(';')[1].split('=')[1].replace('"', '').replace('"', '');
        filename = decodeURI(filename);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        link.remove();
      } else {
        handleKnownException(response);
      }
    },
    handleKnownException(response) {
      var reader = new FileReader();
      reader.onload = function () {
        if (reader.result != null) {
          const responseData = JSON.parse(reader.result);
          if (responseData.code == 500) {
            alert(responseData.msg);
          }
        }
      }
      reader.readAsText(response.data);
    },
    async exportToPDF() {
      console.log('Запрос на экспорт в DOCX: ');
      const config = {
        responseType: 'blob',
        params: {
          group: this.$route.params.id_group, 
          period: this.$route.params.id_period,
          student: this.student.id,
          report: this.student.mentor_report.id || null,
        },
      }
      await this.axios.get('/assessment/export/reportmentor/docx', config).then((response) => {
        this.resolveBlob(response)
        // console.log(response);
        // saveAs(response.data, `${this.student.user.first_name}.docx`);
      });
    }
  },
  computed: {
  // подключение переменной авторизированного пользователя из store
  ...mapGetters(['authUser', 'isAdmin']),
  
  },
}
</script>
  
<style scoped>
.grade-wrapper {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  row-gap: 10px;
}

.grade-item {
  display: flex;
  align-items: center;
  column-gap: 10px;
}
.grade-value {
  border: 1px solid #a7a7a78a;
  padding: 5px 10px;
  min-height: 40px;
  border-radius: 5px;
  min-width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
.criteria-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.report-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
}

.report-item:hover {
  transition: 1s;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.4);
}

.student-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
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
  margin-top: 10px;
  border-bottom: 0.5px solid #a7a7a78a;
}
.assess-title:hover {
  font-weight: 700;
}
/* .assess-title::after {
  content: '   \25BC';
} */
.student-assessment {
  margin-top: 10px;
  display: flex;
  column-gap: 5px;
}

.achievements-wrapper {
  flex-grow: 1;
  min-height: 100px;
  margin-bottom: 10px;
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
}

.assess-item {
  display: flex;
  align-items: center;
  border-bottom: 0.5px solid #a7a7a78a;
  padding: 0 5px;
}

.assess-criterion:hover {
  font-weight: 700;
  cursor: pointer;
}

.assess-mark {
  font-weight: 700;
  margin-left: auto;
}

.student-report {
  margin-top: 10px;
}
.events-title {
  margin-top: 10px;
  border-radius: 10px;
  padding: 10px;
}
.event-item {
  margin-top: 5px;
  padding: 10px;
  border: 0.5px solid #a7a7a78a;
  border-radius: 10px;
}
.events-teacher-title {
  margin: 10px 0;
}
.events-no {
  padding: 10px;
}
.subject-reports-title {
  margin: 10px 0;
  text-transform: uppercase;
  font-size: 1.2em;
}
.subject-reports {
  margin-top: 10px;
}
.subject-title {
  margin-left: 10px;
}
.accordion-button {
  background: #ebebeb;
  color: #000000;
}
.check-yes {
  background: #d3dd67;
}
.subject-criteria{
  border: 1px solid #a7a7a78a;
  border-radius: 5px;
  padding: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.criteria-item {
  display: flex;
  align-items: center;
}
.criteria-value {
  border: 1px solid #a7a7a78a;
  padding: 5px 10px;
  margin-left: 10px;
  min-height: 40px;
  border-radius: 5px;
  min-width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
.subject-report {
  margin-top: 10px;
  font-style: italic;
}
.subject-teacher {
  display: flex;
}
.teacher-name {
  margin-left: auto;
}
</style>