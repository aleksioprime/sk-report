<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Итоговые оценки</div>
      <button v-if="editable && !editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div class="grade-wrapper">
            <div class="grade-item">
              <div class="grade-title">Итоговая оценка РФ: </div>
              <div class="grade-value">{{ report.final_grade }}</div>
            </div>
            <div class="grade-item" v-if="program == 'dp'">
              <div class="grade-title">Итоговая оценка IB: </div>
              <div class="grade-value">{{ report.final_grade_ib }}</div>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="field-description">Выставите итоговую оценку</div>
          <div class="assessment-mark-wrapper edit">
            <div class="assessment-mark-item">
              <div class="letter">РФ: </div>
              <mark-choice v-model="editData.final_grade" :max_mark="5" :name="'final_grade'"/>
            </div>
            <div class="assessment-mark-item" v-if="program == 'dp'">
              <div class="letter">IB: </div>
              <mark-choice v-model="editData.final_grade_ib" :max_mark="7" :name="'final_grade_ib'"/>
            </div>
          </div>
          <div class="field-buttons">
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'ReportFielAssessmentDP',
  props: {
    report: { 
      type: Object, 
      default: {}
    },
    editable: { type: Boolean, default: false },
    program: { type: String }
  },
  data() {
    return {
      editMode: false,
      editData: {},
    }
  },
  methods: { 
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData);
    },
    cancelField() {
      this.editData = {}
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      this.editData.final_grade = this.report.final_grade;
      this.editData.final_grade_ib = this.report.final_grade_ib;
    },

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
.grade-wrapper.edit {
  border: 1px solid var(--bs-secondary);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
}
.grade-wrapper.predict {
  border: 1px solid var(--my-focus);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
  flex-wrap: nowrap;
}
.grade-item {
  flex-basis: 23%;
  display: flex;
  align-items: center;
  column-gap: 10px;
}
.grade-wrapper.predict .grade-value {
  margin-left: 10px;
  width: 100%;
}
.grade-item input {
  width: 70px;
}
.grade-item label {
  width: 100%;
  margin-right: 10px;
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
@media screen and (max-width: 992px) {
  .grade-item {
    flex-basis: 45%;
  }
  .grade-value {
    margin-left: auto;
  }
  .grade-wrapper {
    justify-content: space-between;
  }
}
.assessment-mark-wrapper {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  row-gap: 10px;
  column-gap: 10px;
  justify-content: space-between;
}

.assessment-mark-item {
  display: flex;
  align-items: center;
  flex-basis: 23%;
}
@media screen and (max-width: 992px) {
  .assessment-mark-item  {
    flex-basis: 45%;
  }
}
@media screen and (max-width: 768px) {
  .assessment-mark-item  {
    flex-basis: 100%;
  }
}
.assessment-mark-item .letter {
  font-size: 1.2em;
  font-weight: 700;
  margin-right: 10px;
  min-width: 40px;
}
</style>