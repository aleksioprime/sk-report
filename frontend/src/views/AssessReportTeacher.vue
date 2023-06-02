<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты учителей</template>
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
      <div class="col-md my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentReportPeriod">
          <option :value="{}"> Все периоды </option>
          <option v-for="(period, i) in reportPeriods" :key="period.id" :value="period">
            Репорты за {{ period.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="program-wrapper">
      <div class="radiobutton" v-for="plan in currentStudyYear.academic_plan" :key="plan.id">
        <input type="radio" name="program" :value="plan" :id="`program-${plan.id}`" @change="choicePlan" v-model="currentPlan">
        <label :for="`program-${plan.id}`">
          <div>{{ plan.name_rus }}</div>
        </label>
      </div>
    </div>
    <div class="block-class mt-3">
      <div class="radiobutton">
        <input type="radio" name="year" :value="null" id="year-null" v-model="currentYearId">
        <label for="year-null">Все классы</label>
      </div>
      <div v-for="year in years" :key="year.id" class="radiobutton">
        <input type="radio" name="year" :value="year.id" :id="'year-' + year.id"
          v-model="currentYearId" @change="choiceYear">
        <label :for="'year-' + year.id">{{ year.year_rus }} классы</label>
      </div>
    </div>
    <div class="block-subject mt-3">
      <div class="subject radiobutton">
        <input type="radio" name="subject" :value="null" :id="'subject-x'" v-model="currentSubjectId">
        <label :for="'subject-x'">Предмет не выбран</label>
      </div>
      <div v-for="sb in subjects" :key="sb.id" class="subject radiobutton">
        <input type="radio" name="subject" :value="sb.id" :id="'subject-' + sb.id" v-model="currentSubjectId" @change="choiceSubject">
        <label :for="'subject-' + sb.id">{{ sb.name_rus }}</label>
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
            <!-- <div class="assessment-wrapper" v-if="currentSubjectId">
              <div class="assessment-title">Итоговые оценки по предмету <b>{{ currentSubject.name_rus }}</b>:</div>
              <div class="assessment-period">
                <div class="period-item" :class="{'period-myp-item' : periodClass(year).length == 3}" v-for="period in periodClass(year)" :key="period.id" @click="$router.push(`/assessment/group/${group.id}/period/${period.id}/subject/${currentSubjectId}`)">
                  <div class="period-title">{{ period.number }} {{ period.type }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div> -->
            <div class="report-wrapper" v-if="currentSubjectId">
              <!-- <div class="report-title">Репорты учителя по предмету <b>{{ currentSubject.name_rus }}</b>:</div> -->
              <div class="report-period">
                <div class="period-item" v-for="period in reportPeriods.filter(item => !currentReportPeriod.id || item.id == currentReportPeriod.id)" :key="period.id">
                  <div class="period-title">Репорты за {{ period.name }}</div>
                  <div class="period-info">
                    <div>Предмет: {{ currentSubject.name_rus }}</div>
                    <div><span v-if="group.teachers.length > 1">Учителя:</span><span v-else>Учитель:</span> <span v-for="teacher, index in group.teachers" :key="teacher.id">{{ teacher.full_name }}<span v-if="++index !== group.teachers.length">,&nbsp;</span></span></div>
                  </div>
                  <div class="period-students">
                    <div v-for="student in group.students" :key="student.id" class="report-student" :class="getStyleForStudent(student, group.reports, period.id)">{{ student.short_name }}</div>
                  </div>
                  <button @click="openReportTeacher(group.id, period.id)" class="btn btn-primary period-button mt-2">Перейти к репортам</button>
                </div>
              </div>
            </div>
            <!-- <div v-if="showAllData || authUser.teacher && group.psychologist && group.psychologist.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты психолога <span v-if="group.psychologist">({{ group.psychologist.user.last_name }} {{ group.psychologist.user.first_name }} {{ group.psychologist.user.middle_name }})</span>:</div>
              <div class="psychologist-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/psychologist/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">{{ capitalizeString(period.name) }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div v-if="showAllData || authUser.teacher && group.mentor && group.mentor.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты наставника <span v-if="group.mentor">({{ group.mentor.user.last_name }} {{ group.mentor.user.first_name }} {{ group.mentor.user.middle_name }})</span>:</div>
              <div class="mentor-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/mentor/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">{{ capitalizeString(period.name) }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div> -->
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
import { getGroupsForReportTeacher } from "@/hooks/user/useGroup";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getPeriods } from "@/hooks/assess/usePeriod";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";
import { getClassYearsForReport } from "@/hooks/unit/useClassYear";

import { getAcademicPlan } from "@/hooks/curriculum/useAcademicPlan";

import { mapGetters } from 'vuex';

export default {
  components: {
    
  },
  setup(props) {
    const { academicPlan, fetchGetAcademicPlan } = getAcademicPlan();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { groupsForReportTeacher, isGroupLoading, fetchGetGroupsForReportTeacher } = getGroupsForReportTeacher();
    const { groupedArrayData } = getGroupedArray();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { periods, fetchGetPeriods } = getPeriods();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();
    const { years, fetchGetClassYears } = getClassYearsForReport();

    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      groupsForReportTeacher, isGroupLoading, fetchGetGroupsForReportTeacher,
      groupedArrayData,
      subjects, fetchGetSubjects,
      periods, fetchGetPeriods,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
      years, fetchGetClassYears,
      academicPlan, fetchGetAcademicPlan
    }
  },
  data() {
    return {
      currentSubjectId: null,
      currentLevel: 'ooo',
      currentPlan: {},
      levels: [
        { value: 'noo', name: 'Начальная школа' },
        { value: 'ooo', name: 'Средняя школа' },
        { value: 'soo', name: 'Старшая школа' },
      ],
      showAllData: false,
      currentYearId: null,
    }
  },
  methods: {
    getStyleForStudent(student, reports, period) {
      const studentInReport = reports.find(item => item.student_id == student.id && item.period == period)
      if (studentInReport) {
        if (studentInReport.check_text) {
          return 'check-text'
        }
        return 'check-student'
      }
    },
    capitalizeString(word) {
      return word.charAt(0).toUpperCase() + word.slice(1)
    },
    choicePlan() {
      this.getDataForReports();
      this.currentSubjectId = null;
      localStorage.removeItem('report_teacher_subject');
      this.currentYearId = null;
      localStorage.removeItem('report_teacher_year');
      localStorage.setItem('report_teacher_plan', this.currentPlan.id);
    },
    changeView() {
      this.currentSubjectId = null;
      localStorage.removeItem('report_teacher_subject');
      this.currentYearId = null;
      localStorage.removeItem('report_teacher_year');
      this.getDataForReports();
      if (this.showAllData) {
        localStorage.setItem('report_teacher_all', true);
      } else {
        localStorage.removeItem('report_teacher_all');
      }
    },
    openReportTeacher(group_id, period_id) {
      if (this.showAllData) {
        this.$router.push(`/report/teacher/group/${group_id}/period/${period_id}/subject/${this.currentSubjectId}`)
      } else {
        this.$router.push(`/report/teacher/group/${group_id}/period/${period_id}/subject/${this.currentSubjectId}/author/${this.authUser.teacher.id}`)
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
      this.currentSubjectId = Number(localStorage.getItem('report_teacher_subject')) || null;
      this.currentYearId = Number(localStorage.getItem('report_teacher_year')) || null;
      this.showAllData = Boolean(localStorage.getItem('report_teacher_all')) || false;
      if (Number(localStorage.getItem('report_teacher_plan'))) {
        this.currentPlan = this.currentStudyYear.academic_plan.find(item => item.id == Number(localStorage.getItem('report_teacher_plan')));
      } else {
        this.currentPlan = this.currentStudyYear.academic_plan[1]
      }
    },
    getDataForReports() {
      console.log(this.currentPlan)
      if (this.showAllData) {
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetClassYears({ level: this.currentPlan.level });
          // this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetSubjects({ plan: this.currentPlan.id, need_report: 1 }).finally(() => {
        if (this.currentSubjectId) {
          this.fetchGetGroupsForReportTeacher({ study_year: this.currentStudyYear.id, level: this.currentPlan.level, subject: this.currentSubjectId });
        }
        });
      } else {
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetClassYears({ study_year: this.currentStudyYear.id, teacher: this.authUser.teacher.id, level: this.currentPlan.level });
          // this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetSubjects({ teacher: this.authUser.teacher.id, plan: this.currentPlan.id, need_report: 1 }).finally(() => {
        if (this.currentSubjectId) {
          this.fetchGetGroupsForReportTeacher({ study_year: this.currentStudyYear.id, level: this.currentPlan.level, subject: this.currentSubjectId, teacher: this.authUser.teacher.id });
        }
        });
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
      return this.groupsForReportTeacher.filter(item => {
        if (this.currentYearId) {
          return item.class_year.id == Number(this.currentYearId) 
        } else {
          return item
        }
      });
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
    currentSubject() {
      return this.subjects.find(item => item.id == this.currentSubjectId)
    }
  },
  watch: {
    currentSubjectId() {
      if (this.currentSubjectId) {
        localStorage.setItem('report_teacher_subject', this.currentSubjectId);
        this.fetchGetGroupsForReportTeacher({ study_year: this.currentStudyYear.id, level: this.currentPlan.level, subject: this.currentSubjectId });
      } else {
        this.groupsForReportTeacher = []
        localStorage.removeItem('report_teacher_subject');
      }
    },
    currentYearId() {
      if (this.currentYearId) {
        localStorage.setItem('report_teacher_year', this.currentYearId);
      } else {
        localStorage.removeItem('report_teacher_year');
      }
    }    
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