<template>
  <div class="report-item area">
    <div class="student-header">
      <div class="student-photo">
        <img :src='report.user.photo ? report.user.photo : require("@/assets/img/student.svg")' alt="" width="50">
      </div>
      <div class="student-info">
        <div class="student-name">{{ report.user.last_name }} {{ report.user.first_name }}</div>
      </div>
    </div>
    <div class="student-report">
      <report-field-report id="student-report" :report="report" :dataField="report.psycho_report" @save="fetchSaveReport" :editable="editable"/>
    </div>
    <div class="student-events">
      <div class="events-title selected" data-bs-toggle="collapse" :href="`#collapse-events-${report.id}`" role="button" 
      aria-expanded="false" :aria-controls="`collapse-events-${report.id}`">Участие в мероприятиях</div>
      <report-field-blocks class="collapse" :id="`collapse-events-${report.id}`" :fieldData="report.psycho_report.events" 
      :fieldName="'events'" :defaultItem="defaultEvent" @save="fetchSaveReport" :editable="editable">
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
</template>
  
<script>
import { mapGetters } from 'vuex';
import ReportFieldReport from "@/components/assessment/ReportFieldReport.vue";
import ReportFieldBlocks from "@/components/assessment/ReportFieldBlocks.vue";
export default {
  name: 'ReportTeacherItem',
  components: {
    ReportFieldReport, ReportFieldBlocks
  },
  props: {
    report: {
      type: Object,
      default: {
        group: {},
        user: {},
      }
    },
    period: { Object },
    types: { 
      type: Array,
      default: [],
    },
    levels: { 
      type: Array,
      default: [],
    },
    editable: { type: Boolean, default: false },
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
    fetchSaveReport(data) {
      console.log('Сохранение репорта: ', data);
      let editReportStudents = { ...data }
      editReportStudents.student_id = this.report.id;
      editReportStudents.author_id = this.authUser.teacher.id;
      editReportStudents.id = this.report.psycho_report.id || null
      this.$emit('updateReport', editReportStudents);
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>
  
<style scoped>
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

.dnevnik-title {
  margin-top: 15px;
  padding: 10px;
  border-radius: 10px;
}
.dnevnik-wrapper {
  padding: 10px;
}
.student-criteria {
  margin-top: 10px;
}
.student-report {
  margin-top: 10px;
}
.events-title {
  margin-top: 10px;
  border-radius: 10px;
  padding: 10px;
}
.accordion-button{
  padding: 10px;
}
</style>