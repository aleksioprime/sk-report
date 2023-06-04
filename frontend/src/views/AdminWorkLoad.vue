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
    <!-- Выбор уровня образования -->
    <div class="my-2">
      <select id="levels" class="form-select me-3 mb-2" v-model="currentPlanId">
        <option :value="null">Все учебные планы</option>
        <option v-for="ap in currentStudyYear.academic_plan" :key="ap.id" :value="ap.id">
          {{ ap.name_rus }}
        </option>
      </select>
    </div>
    <!-- Нагрузка учителей -->
    <div class="my-2">
      <div class="collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-workload`" role="button" aria-expanded="false" :aria-controls="`#collapse-workload`">Общая нагрузка учителей кафедры</div>
      <div class="p-2 collapse" :id="`collapse-workload`"> 
        <div v-for="wlTeacher, index in workLoadTeachers" :key="index" class="mt-2">
          <div><b>{{ wlTeacher.teacher.full_name }}</b> (Общая нагрузка: {{ getWordHour(wlTeacher.hours) }})</div>
          <div v-for="wlSubject, iSub in wlTeacher.workload" :key="iSub">
            <div class="workload-wrapper">
              <div>{{ ++iSub }}. {{ wlSubject.subject }} ({{ getWordHour(wlSubject.hours) }}):&nbsp;</div>
              <div v-for="sh, index in wlSubject.group_hours" :key="index">
                <span v-for="group, i in sh.groups" :key="group">{{ group }}
                  <span v-if="++i !== sh.groups.length">,&nbsp;</span></span> - <span>
                    {{ getWordHour(sh.hours) }}<span v-if="++index !== wlSubject.group_hours.length">,&nbsp;</span></span>
              </div>.
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="subject-wrapper" v-if="!isSubjectLoading">
      <div v-for="ap in filteredAcademicPlans" :key="ap.id">
        <div class="wrapper-title"><h2>{{ ap.name_rus }}</h2></div>
        <div class="subject-noo-wrapper" v-if="filteredSubject(ap.id).length">
          <work-load-item v-for="subject in filteredSubject(ap.id)" :key="subject.id" :subject="subject" @deleteItem="showWorkLoadDelete">
            <template v-slot:form>
              <button class="icon icon-add mt-2" v-show="editableSubject != subject.id" @click="showWorkLoadAdd(subject)"></button>
              <work-load-form v-if="editableSubject == subject.id" :groups="groups" :subjects="subjects" :teachers="teachers"
                :editableData="editableData" :deletionMode="deletionMode" @apply="applyWorkLoad" @cancel="cancelWorkLoad"/>
            </template>
          </work-load-item>
        </div>
        <div class="subject-wrapper area" v-else>Нет данных</div>
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
    const { workLoadSubjects, isSubjectLoading, fetchGetWorkLoadSubjects } = getWorkLoadSubjects();
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
      workLoadSubjects, isSubjectLoading, fetchGetWorkLoadSubjects,
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
      currentPlanId: null,
    }
  },
  methods: {
    getWordHour(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} часов`;
      if (number > 1 && number < 5) return `${count} часа`;
      if (number == 1) return `${count} час`;
      return `${count} часов`;
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
    },
    changeDepartment() {
      this.fetchGetWorkLoadSubjects({ department: this.currentDepartment, study_year: this.currentStudyYear.id }).finally(() => {});
    },
    filteredSubject(id) {
      return this.workLoadSubjects.filter(item => item.syllabus.map(obj => obj.academic_plan).includes(id))
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
    filteredAcademicPlans() {
      if (this.currentPlanId) {
        return this.currentStudyYear.academic_plan.filter(item => item.id == this.currentPlanId)
      } else {
        return this.currentStudyYear.academic_plan
      }
    },
    workLoadTeachers() {
      let wlTeachers = []
      this.workLoadSubjects.forEach(subject => {
        subject.workload.forEach(item => {
          const indexTeacher = wlTeachers.findIndex(wl_teacher => wl_teacher.teacher.id == item.teacher.id)
          if (indexTeacher != -1) {
            wlTeachers[indexTeacher].hours += item.hours
            const indexSubject = wlTeachers[indexTeacher].workload.findIndex(wl => wl.subject == item.subject_name)
            if (indexSubject != -1) {
              wlTeachers[indexTeacher].workload[indexSubject].hours += item.hours
              wlTeachers[indexTeacher].workload[indexSubject].group_hours.push({ groups: item.groups.map(gr => gr.group_name), hours: item.hours })
            } else {
              wlTeachers[indexTeacher].workload.push({ subject: item.subject_name, hours: item.hours, group_hours: [{ groups: item.groups.map(gr => gr.group_name), hours: item.hours }] })
            }            
          } else {
            wlTeachers.push({ teacher: item.teacher, hours: item.hours, workload: [{ subject: item.subject_name, hours: item.hours, group_hours: [{ groups: item.groups.map(gr => gr.group_name), hours: item.hours }] }] })
          }
        })
      })
      return wlTeachers
    }
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
.workload-wrapper {
  display: flex;
  flex-wrap: wrap;
}
.workload-item {
  padding: 5px;
  border: 1px solid #000;
  border-radius: 5px;
}
</style>