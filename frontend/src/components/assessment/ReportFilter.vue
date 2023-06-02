<template>
  <div class="block-filter">
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear" @change="resetQuery">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
            {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <!-- Выбор периодов обучения -->
    <div class="block-period">
      <div v-for="pr in reportPeriods" :key="pr.id" class="period">
        <input type="radio" name="period" :value="pr" :id="'period-' + pr.id"
          v-model="currentReportPeriod" @change="handleQuery">
        <label :for="'period-' + pr.id">
        <div class="period-title">{{ pr.number }} период</div>
        <div class="period-item-date">{{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }}</div>
        </label>
      </div>
    </div>
    
    <div class="row">
      <!-- Выбор класса -->
      <div class="col-md">
        <select id="class-group" class="form-select me-3 mb-2" v-model="currentGroup" @change="handleQuery">
          <option :value="null">Выберите класс</option>
          <option v-for="(gr, i) in groups" :key="i" :value="gr.id">
              {{ gr.class_year }}{{ gr.letter }} класс
          </option>
        </select>
      </div>
    </div>
    <!-- Выбор предмета -->
    <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubject" @change="handleQuery">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getTeachers } from "@/hooks/user/useUser";
import { getGroups } from "@/hooks/user/useGroup";

export default {
  props: {
    
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { groups, fetchGetGroups } = getGroups();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
      subjects, fetchGetSubjects,
      groups, fetchGetGroups,
      teachers, isTeacherLoading, fetchGetTeachers
    }
  },
  data() {
    return {
      currentGroup: null,
      currentSubject: null,
    }
  },
  methods: {
    resetQuery() {
      this.currentSubject = null;
      this.currentGroup = null;
    },
    getClassGroups() {
      this.currentGroup = null;
      this.handleQuery();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, class_year: this.currentClassYear});
    },
    handleQuery(event) {
      this.$emit('updateFetch', { 
        study_year: this.currentStudyYear.id,
        period: this.currentReportPeriod,
        subject: this.currentSubject,
        group: this.currentGroup,
      });
    },
    handleStudyYear() {
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear })
    }
  },
  mounted() {
    this.fetchGetSubjects({ program: 'MYP' });
    this.fetchGetStudyYears().finally(() => {
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear }).finally(() => {
        this.fetchGetGroups({ study_year: this.currentStudyYear.id });
        this.currentSubject = this.$route.params.id_subject;
        this.currentGroup = this.$route.params.id_group;
        this.handleQuery();
      })
    });
    
  },
  watch: {
    
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
  margin-top: 5px;
}

</style>