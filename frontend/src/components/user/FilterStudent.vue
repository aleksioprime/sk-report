<template>
  <div class="block-filter">
    <div class="d-flex my-2">
      <input class="form-control" type="search" name="search" id="search" placeholder="Найти по фамилии..."
        v-model="searchValue" @search="handleSearch">
      <button class="btn btn-primary ms-2" @click="handleSearch" :disabled="!searchValue">Найти</button>
    </div>
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentYear" @change="handleStudentYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import { getStudyYears } from "@/hooks/assess/useStudyYear";
export default {
  props: {
    currentYear: {
      type: Object,
      default: {}
    }
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    return {
      studyYears, currentStudyYear, fetchGetStudyYears
    }
  },
  data() {
    return {
      searchValue: null,
    }
  },
  methods: {
    handleSearch(event) {
      this.$emit('searchUser', this.searchValue);
    },
    handleStudentYear(event) {
      this.$emit('update:currentYear', this.currentYear);
    },
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.$emit('update:currentYear', this.currentStudyYear);
    });

  },
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
}
</style>