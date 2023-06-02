<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Итоговые баллы по критериям</div>
      <button v-if="editable && !editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div class="criteria-wrapper">
            <div class="criteria-item">
              <div class="criteria-a">{{ criteria.criterion_a.letter }}. {{ criteria.criterion_a.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_a }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-b">{{ criteria.criterion_b.letter }}. {{ criteria.criterion_b.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_b }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-c">{{ criteria.criterion_c.letter }}. {{ criteria.criterion_c.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_c }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-d">{{ criteria.criterion_d.letter }}. {{ criteria.criterion_d.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_d }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-d">Сумма баллов: </div>
              <div class="criteria-value">{{ this.report.criterion_summ || '-' }} / {{ this.report.criterion_count * 8 || '-' }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-d">Оценка РФ: </div>
              <div class="criteria-value">{{ this.report.criterion_rus }}</div>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="achievements-title collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-achievements-${report.id}`" role="button" aria-expanded="false" :aria-controls="`collapse-achievements-${report.id}`">
            Выставление баллов по предметным достижениям
          </div>
          <div :id="`collapse-achievements-${report.id}`" class="collapse">
            <div class="row">
              <div class="criterion-wrapper col-sm mt-2">
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_a" id="criterion_a" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_a" class="criterion-a">A</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_b" id="criterion_b" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_b" class="criterion-b">B</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_c" id="criterion_c" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_c" class="criterion-c">C</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_d" id="criterion_d" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_d" class="criterion-d">D</label>
                </div>
              </div>
              <div class="col-sm-4 mt-2">
                <select class="form-select" name="level-subject" id="level-subject" v-model="currentYear" @change="changeYear">
                  <option :value="{}">Выберите уровень</option>
                  <option v-for="lvl in levels" :key="lvl.id" :value="lvl">{{ lvl.name_eng }}</option>
                </select>
              </div>
            </div>
            <div class="achievements-wrapper">
              <div v-if="currentCriterion.id && currentYear.id">
                <div class="achievements-filter">
                  <div>Уровни достижений по критерию <b>{{ this.currentCriterion.letter }}. {{ this.currentCriterion.name_eng }}</b> за <b>{{ currentYear.name_eng }}</b>:</div>
                </div>
                <div class="accordion" :id="`accordion-${currentCriterion.id}`">
                  <div class="accordion-item" v-for="objective in filteredObjectivesByYearAndCriterion" :key="objective.id">
                    <h2 class="accordion-header">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-objective-${objective.id}`" aria-expanded="true" :aria-controls="`collapse-objective-${objective.id}`">
                        {{ objective.strand.letter_i }}. {{ objective.name_eng }}
                      </button>
                    </h2>
                    <div :id="`collapse-objective-${objective.id}`" class="accordion-collapse collapse" :data-bs-parent="`#accordion-${currentCriterion.id}`">
                      <div class="accordion-body">
                        <div v-if="objective.achievelevel.length">
                          <div class="radio-check">
                            <input type="radio" :name="`achievement-${objective.id}`" :value="null" :id="`achievement-${objective.id}-none`" v-model="currentAchievement[`${objective.id}`]">
                            <label :for="`achievement-${objective.id}-none`" class="achievement-item">
                              <div class="achievement-name">Стрэнд не участвует в оценке</div>
                              <div class="achievement-point">-</div>
                            </label>
                          </div>
                          <div class="radio-check">
                            <input type="radio" :name="`achievement-${objective.id}`" :value="0" :id="`achievement-${objective.id}-0`" v-model="currentAchievement[`${objective.id}`]">
                            <label :for="`achievement-${objective.id}-0`" class="achievement-item">
                              <div class="achievement-name">The student does not reach a standard described by any of the descriptors below</div>
                              <div class="achievement-point">0</div>
                            </label>
                          </div>
                          <div v-for="ach in objective.achievelevel" :key="ach.id">
                            <div class="radio-check">
                              <input type="radio" :name="`achievement-${objective.id}`" :value="ach.id" :id="`achievement-${objective.id}-${ach.id}`" v-model="currentAchievement[`${objective.id}`]">
                              <label :for="`achievement-${objective.id}-${ach.id}`" class="achievement-item">
                                <div class="achievement-name">The student {{ ach.name_eng }}</div>
                                <div class="achievement-point">{{ ach.point - 1 }} - {{ ach.point }}</div>
                              </label>
                            </div>
                          </div>
                        </div>
                        <div v-else>Нет данных</div>
                      </div> 
                    </div>
                  </div>
                  <button class="field-btn-done mt-2" @click="saveAchievementField">Рассчитать</button>
                </div>
              </div>
            </div>         
            <div>Рассчитанные баллы по предметным достижениям:</div>
            <div class="criteria-wrapper predict">
              <div class="criteria-item predict">
                <div class="criteria-a">{{ criteria.criterion_a.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('A') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-b">{{ criteria.criterion_b.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('B') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-c">{{ criteria.criterion_c.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('C') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-d">{{ criteria.criterion_d.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('D') }}</div>
              </div>
            </div> 
            <button class="field-btn-done mt-2" @click="autoFieldAchievement">Выставить</button>      
          </div>
          <div class="field-description mt-2">Выставите итоговые баллы по критериям вашей предметной области <b>{{ report.subject.group_ib.name_eng }}</b></div>
          <div class="assessment-mark-wrapper edit">
            <div class="assessment-mark-item">
              <div class="letter">{{ criteria.criterion_a.letter }}: </div>
              <mark-choice v-model="editData.criterion_a" :max_mark="8" :name="'a'"/>
            </div>
            <div class="assessment-mark-item">
              <div class="letter">{{ criteria.criterion_b.letter }}: </div>
              <mark-choice v-model="editData.criterion_b" :max_mark="8" :name="'b'"/>
            </div>
            <div class="assessment-mark-item">
              <div class="letter">{{ criteria.criterion_c.letter }}: </div>
              <mark-choice v-model="editData.criterion_c" :max_mark="8" :name="'c'"/>
            </div>
            <div class="assessment-mark-item">
              <div class="letter">{{ criteria.criterion_d.letter }}: </div>
              <mark-choice v-model="editData.criterion_d" :max_mark="8" :name="'d'"/>
            </div>
          </div>
          <div class="field-buttons">
            <!-- <button class="field-btn-done" @click="autoFieldPeriod">Auto: периоды</button> -->
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
import { getObjectives } from "@/hooks/unit/useObjective";
import { getLevels } from "@/hooks/unit/useLevel";
import MarkChoice from '../UI/MarkChoice.vue';

export default {
  components: { MarkChoice },
  name: 'ReportFieldCriteria',
  props: {
    report: { 
      type: Object, 
      default: {}
    },
    criteria: {
      type: Object,
    },
    avg_criteria: {
      type: Object,
    },
    editable: { type: Boolean, default: false },
  },
  setup(props) {
    const { objectives, fetchGetObjectives } = getObjectives();
    const { levels, fetchGetLevels } = getLevels();
    return {
      objectives, fetchGetObjectives,
      levels, fetchGetLevels,
    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
      currentYear: {},
      currentCriterion: {},
      currentAchievement: {}
    }
  },
  methods: {
    getPredictCriteriaMark(criterion) {
      let answer = null
      if (criterion == 'A') {
        answer = this.report.predict[this.criteria.criterion_a.id].sum_points / this.report.predict[this.criteria.criterion_a.id].count_points
      } else if (criterion == 'B') {
        answer = this.report.predict[this.criteria.criterion_b.id].sum_points / this.report.predict[this.criteria.criterion_b.id].count_points
      } else if (criterion == 'C') {
        answer = this.report.predict[this.criteria.criterion_c.id].sum_points / this.report.predict[this.criteria.criterion_c.id].count_points
      } else if (criterion == 'D') {
        answer = this.report.predict[this.criteria.criterion_d.id].sum_points / this.report.predict[this.criteria.criterion_d.id].count_points
      } else {
        return 'E'
      }
      return answer ? Math.round(answer) : null
    },
    getCurrentAchievement() {
      this.filteredObjectivesByYear.forEach((item) => {
        const findedAchievement = this.report.achievements.find(obj => item.id == obj.objective && obj.level == this.currentYear.id)
        if (findedAchievement) {
          if (findedAchievement.achievement) {
            this.currentAchievement[`${item.id}`] = findedAchievement.achievement
          } else {
            this.currentAchievement[`${item.id}`] = 0
          }
        } else {
          this.currentAchievement[`${item.id}`] = null
        }
      })
    },
    changeYear() {
      this.currentAchievement = {}
    },
    changeCriterion() {
    },
    saveField() {
      this.editMode = false;
      for (let key in this.editData) {
        this.editData[key] = this.editData[key]
      }
      this.$emit('save', this.editData);
    },
    saveAchievementField() {
      const fetchData = {
        achievements: []
      }
      for (let key in this.currentAchievement) {
        if (this.currentAchievement[key] == 0) {
          fetchData.achievements.push({ objective_id: key })
        } else if (this.currentAchievement[key] != null) {
          fetchData.achievements.push({ objective_id: key, achievement_id: this.currentAchievement[key] })
        }
      }
      console.log(fetchData);
      this.$emit('save', fetchData);
    },
    cancelField() {
      this.objectives = [];
      this.currentAchievement = {};
      this.currentCriterion = {};
      this.editData = {};
      this.editMode = false;
    },
    setValidMark(rawMark) {
      if (rawMark > 8) {
        return 8
      } else if (rawMark >= 0 && rawMark <= 8) {
        return Number(rawMark)
      } else if (rawMark < 0) {
        return 0
      } else {
        return null
      }
    },
    editField() {
      this.editMode = true;
      this.editData.criterion_a = this.report.criterion_a;
      this.editData.criterion_b = this.report.criterion_b
      this.editData.criterion_c = this.report.criterion_c;
      this.editData.criterion_d = this.report.criterion_d;
      this.fetchGetLevels({ subject: this.$route.params.id_subject }).finally(() => {
        this.currentYear = this.levels.find(item => item.class_year.includes(this.report.year.id))
        this.fetchGetObjectives({ subject: this.$route.params.id_subject }).finally(() => {
          this.getCurrentAchievement();
          this.currentCriterion = this.criteria.criterion_a
        })
      });
    },
    autoFieldPeriod() {
      this.editData.criterion_a = this.avg_criteria.criterion_a;
      this.editData.criterion_b = this.avg_criteria.criterion_b;
      this.editData.criterion_c = this.avg_criteria.criterion_c;
      this.editData.criterion_d = this.avg_criteria.criterion_d;
    },
    autoFieldAchievement() {
      this.editData.criterion_a = this.getPredictCriteriaMark('A');
      this.editData.criterion_b = this.getPredictCriteriaMark('B');
      this.editData.criterion_c = this.getPredictCriteriaMark('C');
      this.editData.criterion_d = this.getPredictCriteriaMark('D');
    }
  },
  computed: {
    filteredObjectivesByYear() {
      return this.objectives.filter(item => item.level.id == this.currentYear.id)
    },
    filteredObjectivesByYearAndCriterion() {
      return this.filteredObjectivesByYear.filter(item => item.strand.criterion.id == this.currentCriterion.id)
    }
  }
}
</script>
<style scoped>
.criteria-wrapper {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  row-gap: 10px;
}
.criteria-wrapper.edit {
  border: 1px solid var(--bs-secondary);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
}
.criteria-wrapper.predict {
  border: 1px solid var(--my-focus);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
  flex-wrap: nowrap;
}
.criteria-item {
  display: flex;
  align-items: center;
}
.criteria-wrapper.predict .criteria-value {
  margin-left: 10px;
  width: 100%;
}
/* .criteria-item input {
  width: 70px;
}
.criteria-item label {
  width: 100%;
  margin-right: 10px;
} */
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
@media screen and (max-width: 992px) {
  .criteria-item {
    flex-basis: 45%;
  }
  .criteria-value {
    margin-left: auto;
  }
  .criteria-wrapper {
    justify-content: space-between;
  }
}
.criterion-wrapper {
  display: flex;
  column-gap: 5px;
}
.criterion-wrapper div:hover {
  background: var(--my-focus) !important;
  cursor: pointer;
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
}
.accordion-button{
  padding: 10px;
}
.achievements-wrapper {
  flex-grow: 1;
  margin-bottom: 10px;
}
.achievements-filter {
  margin: 10px 0;
  display: flex;
  align-items: center;
  /* padding: 10px 0; */
  border-radius: 10px;
}
.achievements-title {
  padding: 10px;
  border-radius: 5px;
}
.achievements-filter select{
  margin-left: 10px;
  max-width: 200px;
}
.achievement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  column-gap: 10px;
  font-size: 0.8em;
}
.achievement-point {
  min-width: 100px;
  padding: 5px;
  border: 0.5px solid #a7a7a78a;
  text-align: center;
}
.radiobutton input[type=radio]:checked + label.criterion-a {
	background: #F26728 !important;
}
.radiobutton input[type=radio]:checked + label.criterion-b {
	background: #CDDC29 !important;
}
.radiobutton input[type=radio]:checked + label.criterion-c {
	background: #5C2D85 !important;
  color: #fff !important;
}
.radiobutton input[type=radio]:checked + label.criterion-d {
	background: #FED107 !important;
}
.radiobutton label {
  font-size: 1em;
}

/* Кнопки из радиокнопок */
.radio-check input[type=radio] {
	display: none;
}
.radio-check label {
  height: 100%;
  display: flex;
	cursor: pointer;
	padding: 10px;
	border: 1px solid #999;
	border-radius: 10px;
	user-select: none;
}
 
.radio-check input[type=radio]:checked + label {
	background: var(--my-focus);
  color: #000
}

.radio-check label:hover {
	color: #666;
}
.accordion-body {
  padding: 10px;
}
.field-buttons {
  display: flex;
  flex-wrap: wrap;
  row-gap: 5px;
  margin-top: 20px;
}
</style>