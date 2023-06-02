<template>
  <div>
    <!-- Блок фильтрации юнитов MYP по подразделению и учителю -->
    <div class="row border-bottom mb-2">
      <div class="col-md">
        <select id="department" class="form-select me-3 mb-2" v-model="queryDepartment">
          <option :value="''" selected>Все подразделения</option>
          <option v-for="(department, i) in departments" :key="i" :value="department.id">
            {{ department.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <select id="subject" class="form-select me-3 mb-2" v-model="queryTeacher">
          <option :value="''" selected>Все учителя</option>
          <option v-for="(teacher, i) in teachersFromDepartment" :key="i" :value="teacher.id">
            {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
  import { getTeachersFromDepartment } from "@/hooks/unit/filterUnitMYPData";
  import { toRefs } from 'vue';
  
  export default {
    name: 'UnitDPList',
    components: {
      
    },
    props: {
      departments: Array,
      teachers: Array,
    },
    setup(props) {
      const { teachers } = toRefs(props);
      // Фильтрация списка учителей по выбранному подразделению
      const { teachersFromDepartment, queryDepartment } = getTeachersFromDepartment(teachers);
      return {
        teachers, teachersFromDepartment, queryDepartment
      }
    },
    data() {
      return {
        queryTeacher: '',
      }
    },
  }
</script>

<style scoped>

</style>