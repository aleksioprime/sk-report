<template>
  <div>
    <div class="student-wrapper">
      <h3>{{ group.class_year.year_rus }}{{ group.letter }} класс ({{ getWordStudent(group.count) }})</h3>
      <div class="student-left">
        <h5>Оставшиеся в списке студенты <small>({{ getWordStudent(filterStudents.length) }})</small></h5>
        <select class="form-select" multiple v-model="currentStudentsGroup" size="10">
          <option v-for="(st, index) in filterStudents" :key="st.id" :value="st">
            {{ ++index }}. {{ st.user.last_name }} {{ st.user.first_name }}</option>
        </select>
      </div>
      <div class="student-arrow">
        <button class="btn btn-success my-2" @click="addStudentsToWork" :disabled="!currentStudentsGroup.length">&#8595;</button>
        <button class="btn btn-danger my-2" @click="deleteStudentsFromWork" :disabled="!currentStudentsWork.length">&#8593;</button>
      </div>
      <div class="student-right">
        <h5>Добавленные в репорты студенты <small>({{ getWordStudent(reportStudents.length) }})</small></h5>
        <select class="form-select" multiple v-model="currentStudentsWork" size="10">
          <option v-for="(st, index) in reportStudents" :key="st.id" :value="st.id">
            {{ ++index }}. {{ st.student.user.last_name }} {{ st.student.user.first_name }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    reportStudents: {
      type: Array,
      default: () => []
    },
    group: {
      type: Object,
      default: {
        students: [],
      }
    },
  },
  data() {
    return {
      currentStudentsWork: [],
      currentStudentsGroup: [],
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
    addStudentsToWork() {
      const result = this.currentStudentsGroup.reduce((result, item) => {
        return [
          ...result,
          {'student': item},
        ]
      }, []);
      console.log(result)

      this.$emit('update:reportStudents', this.reportStudents.concat(result));
      this.currentStudentsGroup = [];
    },
    deleteStudentsFromWork() {
      this.$emit('update:reportStudents', this.reportStudents.filter(item => !this.currentStudentsWork.includes(item.id)));
      this.currentStudentsWork = [];
    },
  },
  mounted() {
    console.log('Текущий класс: ', this.group)
  },
  computed: {
    filterStudents() {
      return this.group.students.filter(item => !this.reportStudents.map(item => item.student.id).includes(item.id))
    }
  },
  watch: {

  }
}
</script>

<style scoped>
.student-wrapper {
  display: flex;
  flex-direction: column;
}
.student-left {

}
.student-arrow {
  display: flex;
  justify-content: center;
  column-gap: 10px;
}
.student-right {

}
</style>