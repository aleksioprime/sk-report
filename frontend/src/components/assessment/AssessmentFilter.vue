<template>
  <div class="block-filter">
    <!-- Выбор текущего года  -->
    <div class="my-2 row">
      <div class="col-md">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
          <option v-for="(study, i) in studyYears" :key="i" :value="study" @change="handleStudyYear">
              {{ study.name }} учебный год
          </option>
        </select>
      </div>
      <div class="col-md">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentProgram" @change="handleProgram">
          <option :value="null">Выберите программу</option>
          <option v-for="(program, i) in studyPrograms" :key="i" :value="program.value" @change="handleQuery">
            {{ program.name_rus }}
          </option>
        </select>
      </div>
    </div>
    <!-- Выбор периодов обучения -->
    <div class="block-period">
      <div v-for="pr in periods" :key="pr.id" class="period radiobutton">
        <input type="radio" name="period" :value="pr" :id="'period-' + pr.id"
          v-model="currentPeriod" @change="handleQuery">
        <label :for="'period-' + pr.id">
          <div class="period-title">{{ pr.number }} {{ pr.type }}</div>
        <div class="period-year">
          <span v-for="(cy, index) in pr.class_year" :key="cy.id">
            {{ cy.year_rus }}<span v-if="cy.program == 'DP'">DP</span>
            <span v-if="index != pr.class_year.length - 1">, </span> </span> класс
        </div>
        <div class="period-item-date">{{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }}</div>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getPeriods } from "@/hooks/assess/usePeriod";

export default {
  props: {
    studyPrograms: { Object },
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { periods, currentPeriod, fetchGetPeriods } = getPeriods();
    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      periods, currentPeriod, fetchGetPeriods
    }
  },
  data() {
    return {
      currentProgram: 'MYP',
    }
  },
  methods: {
    handleProgram() {
      this.fetchGetPeriods({ study_year: this.currentStudyYear, program: this.currentProgram })
    },
    handleQuery(event) {
      this.$emit('updateFetch', { studyYear: this.queryStudyYear, program: this.currentProgram, period: this.currentPeriod });
    },
    handleStudyYear() {
      this.fetchGetPeriods({ study_year: this.currentStudyYear, program: this.currentProgram })
    }
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.fetchGetPeriods({ study_year: this.currentStudyYear, program: this.currentProgram }).finally(() => {
        this.handleQuery();
      })
    });
  },
  computed: {
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
.block-period {
  display: flex;
  align-items: stretch;
  gap: 5px;
  margin-bottom: 10px;
}
.period {
  flex-grow: 1;
}
.period-title {
  font-size: 1.5em;
  font-weight: 700;
}
</style>