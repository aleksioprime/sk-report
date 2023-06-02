<template>
  <div>
    <base-header>
      <template v-slot:header>Учебные предметы</template>
    </base-header>
    <button v-show="!addSubject" class="btn btn-primary" @click="showSubjectAdd">Добавить предмет</button>
    <subject-form v-if="addSubject" :departments="departments" :ib_groups="criteriaGroups" :fgos_groups="subjectGroups"
      :editableData="editableData" :deletionMode="deletionMode" @apply="applySubject" @cancel="cancelSubject"/>
    <div class="mt-3">Количество учебных предметов: {{ filteredSubjects.length }}</div>
    <div v-for="subject in filteredSubjects" :key="subject.id" class="subject-item area">
      <div class=""><h5>{{ subject.name_rus }}</h5></div>
    </div>
  </div>
</template>

<script>
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import SubjectForm from "@/components/curriculum/SubjectForm";
import { getDepartments } from "@/hooks/user/useDepartment";
import { getCriteriaGroups, getSubjectGroups } from "@/hooks/curriculum/useSubjectGroup";

export default {
  name: 'AdminSubject',
  components: {
    SubjectForm
  },
  setup(props) {
    const { groupedArrayData } = getGroupedArray();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { departments, fetchGetDepartments } = getDepartments();
    const { criteriaGroups, fetchCriteriaGroups } = getCriteriaGroups();
    const { subjectGroups, fetchSubjectGroups } = getSubjectGroups();
    return {
      groupedArrayData,
      subjects, fetchGetSubjects,
      departments, fetchGetDepartments,
      criteriaGroups, fetchCriteriaGroups,
      subjectGroups, fetchSubjectGroups
    }
  },
  data() {
    return {
      addSubject: false,
      deletionMode: false,
    }
  },
  methods: {
    showSubjectAdd(data) {
      this.cancelSubject();
      this.fetchGetDepartments();
      this.fetchCriteriaGroups();
      this.fetchSubjectGroups();
      this.addSubject = true;
      this.editableData = { group_ib_id: null, group_fgos_id: null, department_id: null, level: null, type: null };    
    },
    showSubjectEdit() {

    },
    showSubjectDelete(data) {
      this.cancelSubject();
      this.deletionMode = true;
      this.editableSubject = data.subject;
      this.editableData = { id: data.id }
    },
    applySubject(data) {
      if (this.deletionMode) {
        console.log('Удаление предмета: ', data.id)
      } else if (data.id) {
        console.log('Редактирование предмета: ', data)
      } else {
        console.log('Добавление предмета: ', data);
      }
      this.cancelSubject();
    },
    cancelSubject() {
      this.editableSubject = null;
      this.deletionMode = false;
      this.addSubject = false;
      this.editableData = {};
    },
  },
  computed: {
    filteredSubjects() {
      return this.subjects
    }
  },
  mounted() {
    this.fetchGetSubjects({});
    this.fetchGetDepartments();
  }
}
</script>

<style scoped>
.subject-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
}
</style>