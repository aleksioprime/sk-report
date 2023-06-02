<template>
  <div>
    <base-header>
      <template v-slot:link><a href="#" @click="$router.push(`/report/psychologist`)" >Вернуться к выбору класса</a></template>
      <template v-slot:header>Репорты психолога</template>
    </base-header>
    <!-- <report-filter @updateFetch="updateFetch"/> -->
    <div class="col-md mb-2">
      <div>Период репорта: <b>{{ currentReportPeriod.name }}</b></div>
      <div>Класс: <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> ({{ getWordStudent(currentGroup.count) }}) 
        <br>Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }}
        <br><span v-if="currentGroup.psychologist">Психолог: {{ currentGroup.psychologist.user.last_name }} {{ currentGroup.psychologist.user.first_name }} {{ currentGroup.psychologist.user.middle_name }}</span> 
      </div>
    </div>
    <div v-if="!isReportsPsychologistLoading || !firstLoading">
      <div v-if="reportsPsychologist.length" class="report-wrapper">
        <report-psychologist-item v-for="report in reportsPsychologist" :key="report.id" :period="currentReportPeriod"
        :report="report" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport" :editable="currentGroup.psychologist.id == authUser.teacher.id"/>
      </div>
      <div v-else class="report-none">
        Пока нет данных
      </div>
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';
import ReportPsychologistItem from "@/components/assessment/ReportPsychologistItem.vue";
import { getReportPsychologistJournal, getReportsPsychologist, createReportPsychologist, updateReportPsychologist } from "@/hooks/assess/useReportPsychologist";

export default {
  components: {
    ReportPsychologistItem,
  },
  setup(props) {
    // const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportPsychologist } = getReportPsychologistJournal();
    const { reportsPsychologist, isReportsPsychologistLoading, fetchGetReportsPsychologist } = getReportsPsychologist();
    const { createdReportPsychologist, fetchCreateReportPsychologist } = createReportPsychologist();
    const { updatedReportPsychologist, fetchUpdateReportPsychologist } = updateReportPsychologist();
    return {
      currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportPsychologist,
      reportsPsychologist, isReportsPsychologistLoading, fetchGetReportsPsychologist,
      createdReportPsychologist, fetchCreateReportPsychologist,
      updatedReportPsychologist, fetchUpdateReportPsychologist,
    }
  },
  data() {
    return {
      currentReport: {},
      currentFetchData: {},
      currentPeriod: {},
      eventLevels: [
        { value: '0', name: 'Без уровня' },
        { value: '1', name: '1 уровень' },
        { value: '2', name: '2 уровень' },
        { value: '3', name: '3 уровень' },
      ],
      firstLoading: true,
    }
  },
  methods: {
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    // В сигнале на сохранение данные из компонента проверяется, есть ли ID репорта
    // и если его нет, то вызывается функция создания репорта, а если есть, то обновления
    fetchUpdateReport(editingReport) {
      editingReport.period_id = this.currentReportPeriod.id;
      editingReport.year_id = this.currentGroup.class_year.id;
      console.log('Запрос на добавление или обновление данных: ', editingReport)
      if (editingReport.id) {
        this.setStudentReportUpdate(editingReport);
      } else {
        this.setStudentReportCreate(editingReport);
      }
    },
    // Создание нового репорта
    setStudentReportCreate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на добавление данных: ", fetchData);
        this.fetchCreateReportPsychologist(fetchData).finally(() => {
          const index = this.reportsPsychologist.findIndex(item => item.id == fetchData.student_id);
          if (index != -1) {
            this.reportsPsychologist[index].psycho_report = this.createdReportPsychologist
          }
        });
      }
    },
    // Обновление выбранного репорта
    setStudentReportUpdate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на изменение данных: ", fetchData);
        this.fetchUpdateReportPsychologist(fetchData).finally(() => {
          const index = this.reportsPsychologist.findIndex(item => item.psycho_report.id == fetchData.id);
          if (index != -1) {
            this.reportsPsychologist[index].psycho_report = this.updatedReportPsychologist
          }
        });
      }
    },
  },
  mounted() {
    this.fetchGetReportPsychologist({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
    }).finally(() => {
      this.currentFetchData = {
        group: this.currentGroup.id,
        class_year: this.currentGroup.class_year.id,
        period: this.currentReportPeriod.id,
      }
      this.fetchGetReportsPsychologist(this.currentFetchData).finally(() => {
        this.firstLoading = false;
      });
    })
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin', 'isDnevnik']),
  }
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.loader {
  display: flex;
  height: calc(100vh - 200px);
  align-items: center;
  justify-content: center;
}
.report-wrapper {
  margin-top: 20px;
}
.report-none {
  min-height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>