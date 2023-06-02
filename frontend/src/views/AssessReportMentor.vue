<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты наставников</template>
      <template v-slot:extra>
        <div class="toggle" v-if="isAdmin">
          <div class="toggle-item my">
            <input id="show-my" type="radio" :value="false" v-model="showAllData" @change="changeView">
            <label for="show-my">Мои репорты</label>
          </div>
          <div class="toggle-item all">
            <input id="show-all" type="radio" :value="true" v-model="showAllData" @change="changeView">
            <label for="show-all">Просмотр всех репортов</label>
          </div>
        </div>
      </template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="row">
      <div class="col-md my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
          <option v-for="(study, i) in studyYears" :key="i" :value="study">
            {{ study.name }} учебный год
          </option>
        </select>
      </div>
      <div class="col-md-4 my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentReportPeriod">
          <option :value="{}"> Все периоды </option>
          <option v-for="period in reportPeriods" :key="period.id" :value="period">
            Репорты за {{ period.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="block-class mt-3">
      <div class="radiobutton">
        <input type="radio" name="year" :value="null" id="year-null" v-model="currentYearId" @change="choiceYear">
        <label for="year-null">Все классы</label>
      </div>
      <div v-for="year in years" :key="year.id" class="radiobutton">
        <input type="radio" name="year" :value="year.id" :id="'year-' + year.id" v-model="currentYearId" @change="choiceYear">
        <label :for="'year-' + year.id">
          <div>{{ year.year_rus }} классы</div>
        </label>
      </div>
    </div>
    <div v-if="!isGroupLoading">
      <div v-for="(groupsByYear, year) in groupedArrayData(filteredGroups, ['class_year', 'year_rus'])" :key="year">
        <div class="class-group"><h3>{{ year }} классы</h3></div>
        <div v-for="group in groupsByYear" :key="group.id" class="class-item area">
            <div class="row">
              <div class="col-sm">
                <div class="class-title selected"><h5>{{ group.group_name }} класс ({{ getWordStudent(group.count) }})</h5></div>
              </div>
            </div>
            <div class="mentor-period" v-if="group.mentor">
              <div class="period-item" v-for="period in reportPeriods.filter(item => !currentReportPeriod.id || item.id == currentReportPeriod.id)" :key="period.id">
                <div class="period-title">Репорты за {{ period.name }}</div>
                <div class="period-info">Наставник: {{ group.mentor.full_name }}</div>
                <div class="period-students">
                  <div v-for="student in group.students" :key="student.id" class="report-student" :class="getStyleForStudent(student, group.reports, period.id)">{{ student.short_name }}</div>
                </div>
                <button @click="$router.push(`/report/mentor/group/${group.id}/period/${period.id}`)" class="btn btn-primary period-button mt-2">Перейти к репортам</button>
              </div>
            </div>
            <div v-else>Ментор не назначен</div>
        </div>
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

import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getGroupsForReportMentor } from "@/hooks/user/useGroup";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";
import { getClassYearsForReport } from "@/hooks/unit/useClassYear";
import { mapGetters } from 'vuex';

export default {
  components: {
    
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { groupsForReportMentor, isGroupLoading, fetchGetGroupsForReportMentor } = getGroupsForReportMentor();
    const { groupedArrayData } = getGroupedArray();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();
    const { years, fetchGetClassYears } = getClassYearsForReport();

    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      groupsForReportMentor, isGroupLoading, fetchGetGroupsForReportMentor,
      groupedArrayData,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
      years, fetchGetClassYears,
    }
  },
  data() {
    return {
      showAllData: false,
      currentYearId: null,
      currentPeriodId: null,
    }
  },
  methods: {
    getStyleForStudent(student, reports, period) {
      const studentInReport = reports.find(item => item.student_id == student.id && item.period == period)
      if (studentInReport) {
        if (studentInReport.check_text) {
          return 'check-text'
        }
        // return 'check-student'
      }
    },
    capitalizeString(word) {
      return word.charAt(0).toUpperCase() + word.slice(1)
    },
    choiceYear() {
      localStorage.setItem('report_mentor_year', this.currentYearId);
      if (this.showAllData) {
        this.fetchGetGroupsForReportMentor({ study_year: this.currentStudyYear.id, class_year: this.currentYearId });
      } else {
        this.fetchGetGroupsForReportMentor({ study_year: this.currentStudyYear.id, class_year: this.currentYearId, mentor: this.authUser.teacher.id });
      }
    },
    changeView() {
      this.currentYearId = null;
      localStorage.removeItem('report_mentor_year');
      this.getDataForReports();
      if (this.showAllData) {
        localStorage.setItem('report_mentor_all', true);
      } else {
        localStorage.removeItem('report_mentor_all');
      }
    },
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    recoveryDataFromLocalStorage() {
      this.currentYearId = Number(localStorage.getItem('report_mentor_year')) || null;
      this.showAllData = Boolean(localStorage.getItem('report_mentor_all')) || false;
    },
    getDataForReports() {
      if (this.showAllData) {
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetClassYears({});
        this.fetchGetGroupsForReportMentor({ study_year: this.currentStudyYear.id, class_year: this.currentYearId });
      } else {
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetClassYears({ study_year: this.currentStudyYear.id, mentor: this.authUser.teacher.id });
        this.fetchGetGroupsForReportMentor({ study_year: this.currentStudyYear.id, class_year: this.currentYearId, mentor: this.authUser.teacher.id });
      }
    }
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.recoveryDataFromLocalStorage();
      this.getDataForReports();
    });
  },
  computed: {
    filteredGroups() {
      return this.groupsForReportMentor.filter(item => {
          if (this.currentYearId) {
            return item.class_year.id == Number(this.currentYearId) 
          } else {
            return item
          }
      });
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  watch: {
    // showAllData() {
    //   this.getDataForReports();
    // }
  }
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.block-class {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 5px;
  margin-bottom: 10px;
}

.program-wrapper {
  display: flex;
  gap: 5px;
}
.class-title {
  font-weight: 700;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
.class-title h5 {
  margin-bottom: 0;
}
.class-group {
  text-transform: uppercase;
  font-size: 1.5em;
  margin-top: 30px;
}
.class-item {
  padding: 10px;
  margin-top: 5px;
  display: flex;
  flex-direction: column;
}
.class-btns {
  margin-top: 10px;
  display: flex;
}
.class-btns .btn {
  margin-right: 5px;
}
.assessment-wrapper {
  margin-top: 10px;
}
.assessment-title, .report-title {
  font-size: 0.8em;
}
.period-students {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  margin: 10px 0;
}
.report-student {
  padding: 5px;
  border-radius: 5px;
  background: #dadada8a;
  border: 1px solid #dadada8a;
}
.check-text {
  color: #fff;
  background: var(--bs-secondary);
  border: 1px solid var(--bs-secondary);
}
.check-student {
  background: #fff;
  border: 1px solid var(--bs-secondary);
}
.assessment-period, .report-period, .mentor-period, .psychologist-period{
  display: flex;
  flex-direction: column;
  row-gap: 5px;
  margin: 10px 0;
}
.period-myp-item {
  flex-basis: 33% !important;
}
.period-item {
  flex-basis: 49%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #a7a7a78a;
}
.period-title {
  font-size: 1em;
  margin-bottom: 10px;
  text-transform: uppercase;
}
.period-btn {
  border: 1px solid #a7a7a78a;
  border-radius: 5px;
}
.period-btn:hover {
  cursor: pointer;
  background: #a7a7a78a;
}
.period-btn:not(:last-of-type) {
  margin-right: 10px;
}
.report-wrapper {
  margin-top: 0;
}

</style>