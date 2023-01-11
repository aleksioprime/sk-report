<template>
  <div>
    <h1>Работа с юнитом</h1>
    <div class="d-flex">
      <button type="button" class="btn btn-danger ms-auto my-3" @click="showModalUnit()">
        Удалить этот юнит
      </button>
    </div>
    <modal-unit :modalTitle="modalTitle" :del="true" @cancel="hideModalUnit" @delete="deleteUnit">
      <div>Вы действитель хотите удалить этот юнит?</div>
    </modal-unit>
    <div class="d-flex align-items-start mt-3">
      <div class="nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
        <button class="nav-link active" id="v-pills-base-tab" data-bs-toggle="pill" data-bs-target="#v-pills-base"
          type="button" role="tab" aria-controls="v-pills-base" aria-selected="true">Основная информация</button>
        <button class="nav-link" id="v-pills-inquiry-tab" data-bs-toggle="pill" data-bs-target="#v-pills-inquiry"
          type="button" role="tab" aria-controls="v-pills-inquiry" aria-selected="false">Исследование</button>
        <button class="nav-link" id="v-pills-objectives-tab" data-bs-toggle="pill" data-bs-target="#v-pills-objectives"
          type="button" role="tab" aria-controls="v-pills-objectives" aria-selected="false">Образовательные цели</button>
        <button class="nav-link" id="v-pills-learner-profile-tab" data-bs-toggle="pill" data-bs-target="#v-pills-learner-profile"
          type="button" role="tab" aria-controls="v-pills-learner-profile" aria-selected="false">Профиль студента</button>
        <button class="nav-link" id="v-pills-assessment-tab" data-bs-toggle="pill" data-bs-target="#v-pills-assessment"
          type="button" role="tab" aria-controls="v-pills-assessment" aria-selected="false">Оценивание</button>
        <button class="nav-link" id="v-pills-teaching-tab" data-bs-toggle="pill" data-bs-target="#v-pills-teaching"
          type="button" role="tab" aria-controls="v-pills-teaching" aria-selected="false">Стратегии преподавания</button>
      </div>
      <div class="tab-content w-100" id="v-pills-tabContent">
        <div class="tab-pane fade show active" id="v-pills-base" role="tabpanel" aria-labelledby="v-pills-base-tab" tabindex="0">
          <unit-field :text="title" :check="Boolean(unit.title)" @edit="editUnit.title = unit.title" @save="updateUnit">
            <template v-slot:read>{{ unit.title }}</template>
            <template v-slot:edit><field-text-edit v-model="editUnit.title"/></template>
          </unit-field>
          <unit-field :text="subject" :check="Boolean(unit.subject)" @edit="getSubjectsData('ooo', 'base'); editUnit.subject_id = unit.subject.id" @save="updateUnit">
            <template v-slot:read>{{ unit.subject.name_rus }} ({{ unit.subject.group_ib.name_eng }})</template>
            <template v-slot:edit><field-select-edit v-model="editUnit.subject_id" :options="subjects"/></template>
          </unit-field>
          <unit-field :text="hours" :check="Boolean(unit.hours)" @edit="editUnit.hours = unit.hours" @save="updateUnit">
            <template v-slot:read>{{ unit.hours }}</template>
            <template v-slot:edit><field-text-edit v-model="editUnit.hours"/></template>
          </unit-field>
        </div>
        <div class="tab-pane fade show active" id="v-pills-inquiry" role="tabpanel" aria-labelledby="v-pills-inquiry-tab" tabindex="0">

        </div>
        <div class="tab-pane fade show active" id="v-pills-objectives" role="tabpanel" aria-labelledby="v-pills-objectives-tab" tabindex="0">

        </div>
        <div class="tab-pane fade show active" id="v-pills-learner-profile" role="tabpanel" aria-labelledby="v-pills-learner-profile-tab" tabindex="0">

        </div>
        <div class="tab-pane fade show active" id="v-pills-assessment" role="tabpanel" aria-labelledby="v-pills-assessment-tab" tabindex="0">

        </div>
        <div class="tab-pane fade show active" id="v-pills-teaching" role="tabpanel" aria-labelledby="v-pills-teaching-tab" tabindex="0">

        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import axios from 'axios';
import { mapState } from 'vuex'

import { getUnitView } from "@/hooks/unit/myp/edit/getUnitView";
import { getSubjectsMYP } from "@/hooks/unit/myp/getSubjectsMYP";
import { getGrades } from "@/hooks/unit/getGrades";
import { getTeachers } from "@/hooks/unit/getTeachers";
import { getCriteria } from "@/hooks/unit/myp/edit/getCriteria";
import { getAims } from "@/hooks/unit/myp/edit/getAims";
import { getObjectives } from "@/hooks/unit/myp/edit/getObjectives";
import { getKeyConcepts } from "@/hooks/unit/myp/edit/getKeyConcepts";
import { getRelatedConcepts } from "@/hooks/unit/myp/edit/getRelatedConcepts";
import { getGlobalContext } from "@/hooks/unit/myp/edit/getGlobalContext";
import { getExplorations } from "@/hooks/unit/myp/edit/getExplorations";
import { getIBLearnerProfile } from "@/hooks/unit/myp/edit/getIBLearnerProfile";
import FieldTextEdit from '../components/UI/FieldTextEdit.vue';

// import { getAtlSkills } from "@/hooks/getAtlSkills";

export default {
  name: 'UnitPlansView',
  components: {
    FieldTextEdit
    
  },
  setup(props) {
    // Получение функции запроса данных юнита
    const { unit, getUnitData } = getUnitView();
    // Получение функции запроса списка предметов в MYP
    const { subjects, getSubjectsData } = getSubjectsMYP();
    // Получение функции запроса списка учителей
    const { teachers, getTeachersData } = getTeachers();
    // Получение функции запроса списка годов обучения в MYP
    const { grades, getGradesData } = getGrades();
    // Получение функции запроса списка критериев оценки MYP
    const { criteria, getCriteriaData } = getCriteria();
    // Получение функции запроса целей предметных групп
    const { aims, getAimsData } = getAims();
    // Получение функции запроса образовательных задач
    const { objectives, getObjectivesData } = getObjectives();
    // Получение функции запроса ключевых концептов
    const { kconcepts, getKeyConceptsData } = getKeyConcepts();
    // Получение функции запроса связанных концептов
    const { rconcepts, getRelatedConceptsData } = getRelatedConcepts();
    // Получение функции запроса глобальных контекстов
    const { gcontext, getGlobalContextData } = getGlobalContext();
    // Получение функции запроса линий исследования по глобальным контекстам
    const { explorations, getExplorationsData } = getExplorations();
    // Получение функции запроса профиля студента
    const { ibProfiles, getIBLPData } = getIBLearnerProfile();
    // const { atlSkills } = getAtlSkills();
    return {
      unit, getUnitData, subjects, getSubjectsData, teachers, getTeachersData, grades, getGradesData,
      criteria, getCriteriaData, aims, getAimsData, objectives, getObjectivesData, kconcepts, getKeyConceptsData,
      rconcepts, getRelatedConceptsData, gcontext, getGlobalContextData, explorations, getExplorationsData, 
      ibProfiles, getIBLPData
    }
  },
  data() {
    return {
      modalTitle: '',
      editUnit: {},
      title: { label: 'Название юнита', description: 'Напишите название юнита' },
      subject: { 
        label: 'Предмет', 
        description: 'Выберите учебный предмет', 
        warning: 'Внимание: при изменении учебного предмета информация о выбранных критериев оценки, образовательных целях, сопутствующих концептах будет удалена',
      },
      hours: { label: 'Часы', description: 'Укажите количество часов' },
    }
  },
  methods: {
    showModalUnit() {
      this.modalTitle = 'Удаление юнита';
      this.modalUnit.show();
    },
    hideModalUnit() {
      this.modalUnit.hide();
    },
    deleteUnit() {
      const url = `${this.store.state.base.baseAPI}/unitplans/myp/${this.$route.params.id}`;
	    const config = this.store.state.base.configJWT;
      axios.delete(url, config).then(() => {
        this.$router.push('/unitplans');
      });
    },
    updateUnit() {
      const url = `${this.api}/unitplans/myp/${this.$route.params.id}`;
	    const config = this.configJWT;
      axios.put(url, this.editUnit, config).then((response) => {
        this.unit = response.data;
        console.log('Update Unit Success');
      });
    },
  },
  mounted() {
    this.getUnitData(this.$route.params.id);
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
  },
  computed: {
    ...mapState({
      api: state => state.base.baseAPI,
      configJWT: state => state.base.configJWT,
    }),
  },
}
</script>

<style scoped>
  @import '@/assets/css/unitview.css';
</style>