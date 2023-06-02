<template>
  <div>
    <base-header>
      <template v-slot:header>Учебная нагрузка</template>
    </base-header>
    
    <div class="block-departments">
      <div v-for="dp in departments" :key="dp.id" class="department radiobutton">
        <input type="radio" name="department" :value="dp.id" :id="'department-' + dp.id" v-model="currentDepartment"
          @change="changeDepartment">
        <label :for="'department-' + dp.id">
          <!-- <div class="img"><img :src='dp.photo ? dp.photo : require("@/assets/img/sk_report_logo_notext.svg")' alt=""
              width="50" height="50"></div> -->
          <div>{{ dp.name }}</div>
        </label>
      </div>
    </div>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <div class="subject-wrapper">
      <div class="wrapper-title"><h2>Начальная школа</h2></div>
      <div class="subject-noo-wrapper" v-if="nooSubjects.length">
        <work-load-item v-for="subject in nooSubjects" :key="subject.id" :subject="subject" @deleteItem="showWorkLoadDelete">
          <template v-slot:form>
            <button class="icon icon-add mt-2" v-show="editableSubject != subject.id" @click="showWorkLoadAdd(subject)"></button>
            <work-load-form v-if="editableSubject == subject.id" :groups="groups" :subjects="subjects" :teachers="teachers"
              :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/>
          </template>
        </work-load-item>
      </div>
      <div class="subject-wrapper area" v-else>Нет данных</div>
      <!-- <button v-show="!addWorkLoadSubjectNoo" class="btn btn-primary" @click="showWorkLoadSubjectAdd(level='noo')">Добавить нагрузку</button>
        <work-load-form v-if="addWorkLoadSubjectNoo" :groups="groups" :subjects="subjects" :teachers="teachers"
          :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/> -->
      <div class="wrapper-title"><h2>Средняя школа</h2></div>
      <div class="subject-ooo-wrapper" v-if="oooSubjects.length">
        <work-load-item v-for="subject in oooSubjects" :key="subject.id" :subject="subject" @deleteItem="showWorkLoadDelete">
          <template v-slot:form>
            <button class="icon icon-add mt-2" v-show="editableSubject != subject.id" @click="showWorkLoadAdd(subject)"></button>
            <work-load-form v-if="editableSubject == subject.id" :groups="groups" :subjects="subjects" :teachers="teachers"
              :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/>
          </template>
        </work-load-item>
      </div>
      <div class="subject-wrapper area" v-else>Нет данных</div>
      <!-- <button v-show="!addWorkLoadSubjectOoo" class="btn btn-primary" @click="showWorkLoadSubjectAdd(level='ooo')">Добавить нагрузку</button>
        <work-load-form v-if="addWorkLoadSubjectOoo" :groups="groups" :subjects="subjects" :teachers="teachers"
          :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/> -->
      <div class="wrapper-title"><h2>Старшая школа</h2></div>
      <div class="subject-soo-wrapper" v-if="sooSubjects.length">
        <work-load-item v-for="subject in sooSubjects" :key="subject.id" :subject="subject" @deleteItem="showWorkLoadDelete">
          <template v-slot:form>
            <button class="icon icon-add mt-2" v-show="editableSubject != subject.id" @click="showWorkLoadAdd(subject)"></button>
            <work-load-form v-if="editableSubject == subject.id" :groups="groups" :subjects="subjects" :teachers="teachers"
              :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/>
          </template>
        </work-load-item>
      </div>
      <div class="subject-wrapper area" v-else>Нет данных</div>
      <!-- <button v-show="!addWorkLoadSubjectSoo" class="btn btn-primary" @click="showWorkLoadSubjectAdd(level='soo')">Добавить нагрузку</button>
        <work-load-form v-if="addWorkLoadSubjectSoo" :groups="groups" :subjects="subjects" :teachers="teachers"
          :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/> -->
    </div>
  </div>
</template>

<script>
import WorkLoadForm from "@/components/curriculum/WorkLoadForm";

import { getDepartments } from "@/hooks/user/useDepartment";
import { getWorkLoadSubjects, getWorkLoadSubject } from "@/hooks/curriculum/useSubject";
import { createWorkLoad, deleteWorkLoad } from "@/hooks/assess/useWorkLoad";
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getGroups } from "@/hooks/user/useGroup";
import { getTeachers } from "@/hooks/user/useUser";
import { getSubjects } from "@/hooks/curriculum/useSubject";

import WorkLoadItem from "@/components/curriculum/WorkLoadItem.vue";

export default {
  name: 'AdminWorkLoad',
  components: {
    WorkLoadItem, WorkLoadForm
  },
  setup(props) {
    const { departments, fetchGetDepartments } = getDepartments();
    const { workLoadSubjects, fetchGetWorkLoadSubjects } = getWorkLoadSubjects();
    const { workLoadSubject, fetchGetWorkLoadSubject } = getWorkLoadSubject();
    const { createdWorkLoad, fetchCreateWorkLoad } = createWorkLoad();
    const { fetchDeleteWorkLoad } = deleteWorkLoad();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { subjects, fetchGetSubjects } = getSubjects();

    const { groupedArrayData } = getGroupedArray();
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();

    return {
      departments, fetchGetDepartments,
      workLoadSubjects, fetchGetWorkLoadSubjects,
      workLoadSubject, fetchGetWorkLoadSubject,
      createdWorkLoad, fetchCreateWorkLoad,
      fetchDeleteWorkLoad,
      studyYears, currentStudyYear, fetchGetStudyYears,
      groupedArrayData,
      groups, isGroupLoading, fetchGetGroups,
      subjects, fetchGetSubjects,
      teachers, isTeacherLoading, fetchGetTeachers,
    }
  },
  data() {
    return {
      currentDepartment: null,
      editableSubject: null,
      editableData: {},
      deletionMode: false,
      addWorkLoadSubjectNoo: false,
      addWorkLoadSubjectOoo: false,
      addWorkLoadSubjectSoo: false,
    }
  },
  methods: {
    showWorkLoadSubjectAdd(level) {
      this.cancelWorkLoad();
      if (level == 'noo') {
        this.addWorkLoadSubjectNoo = true;
      } else if (level == 'ooo') {
        this.addWorkLoadSubjectOoo = true;
      } else if (level == 'soo') {
        this.addWorkLoadSubjectSoo = true;
      }
      this.fetchGetSubjects({ level: level });
      this.fetchGetTeachers();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: level });
      this.editableData = { groups_ids: [], subject_id: null, teacher_id: null };
    },
    showWorkLoadAdd(data) {
      this.cancelWorkLoad();
      this.subjects = [ data ];
      this.editableSubject = data.id;
      this.fetchGetTeachers();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: data.level });
      this.editableData = { groups_ids: [], subject_id: data.id, teacher_id: null };    
    },
    showWorkLoadEdit() {

    },
    showWorkLoadDelete(data) {
      this.cancelWorkLoad();
      this.deletionMode = true;
      this.editableSubject = data.subject;
      this.editableData = { id: data.id }
    },
    applyWorkLoad(data) {
      if (this.deletionMode) {
        console.log('Удаление нагрузки: ', data.id)
        this.fetchDeleteWorkLoad(data.id).finally(() => {
          this.fetchGetWorkLoadSubjects({ department: this.currentDepartment, study_year: this.currentStudyYear.id });
        })
      } else if (data.id) {
        data.study_year_id = this.currentStudyYear.id
        console.log('Редактирование нагрузки: ', data)
      } else {
        data.study_year_id = this.currentStudyYear.id
        console.log('Добавление нагрузки: ', data);
        this.fetchCreateWorkLoad(data).finally(() => {
          // Обновление данных по текущему предмету
          this.fetchGetWorkLoadSubject(data.subject_id).finally(() => {
            const index = this.workLoadSubjects.findIndex(item => item.id == data.subject_id);
            if (index != -1) {
              this.workLoadSubjects[index] = this.workLoadSubject
            }
          })
        })
      }
      this.cancelWorkLoad();
    },
    cancelWorkLoad() {
      this.editableSubject = null;
      this.deletionMode = false;
      this.editableData = {};
      this.addWorkLoadSubjectNoo = false;
      this.addWorkLoadSubjectOoo = false;
      this.addWorkLoadSubjectSoo = false;
    },
    changeDepartment() {
      this.fetchGetWorkLoadSubjects({ department: this.currentDepartment, study_year: this.currentStudyYear.id }).finally(() => {});
    }
  },
  mounted() {
    this.fetchGetDepartments().finally(() => {
      if (this.departments.length) {
        this.currentDepartment = this.departments[0].id;
      }
      this.fetchGetStudyYears().finally(() => {
        this.fetchGetWorkLoadSubjects({ department: this.currentDepartment, study_year: this.currentStudyYear.id }).finally(() => {});
      })
    });
  },
  computed: {
    nooSubjects() {
      return this.workLoadSubjects.filter(item => item.level == 'noo')
    },
    oooSubjects() {
      return this.workLoadSubjects.filter(item => item.level == 'ooo')
    },
    sooSubjects() {
      return this.workLoadSubjects.filter(item => item.level == 'soo')
    },
  },
}
</script>

<style scoped>
.subject-wrapper {
  margin-top: 10px;
}
.level-title {
  text-transform: uppercase;
  margin: 20px 0;
}
.wrapper-title {
  text-transform: uppercase;
  margin-top: 20px;
}
</style>