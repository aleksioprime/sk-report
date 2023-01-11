<template>
  <div>
    <h1 class="mb-2">Список юнитов</h1>
    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="pills-myp-tab" data-bs-toggle="pill" data-bs-target="#pills-myp" type="button" role="tab" aria-controls="pills-myp" aria-selected="true">MYP</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="pills-dp-tab" data-bs-toggle="pill" data-bs-target="#pills-dp" type="button" role="tab" aria-controls="pills-dp" aria-selected="false">DP</button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <div class="tab-pane fade show active" id="pills-myp" role="tabpanel" aria-labelledby="pills-myp-tab">
        <unit-myp-list :departments="departments" :teachers="teachers"/>
      </div>
      <div class="tab-pane fade" id="pills-dp" role="tabpanel" aria-labelledby="pills-dp-tab">
        <unit-dp-list :departments="departments" :teachers="teachers"/>
      </div>
    </div>
  </div>
</template>

<script>
// Импорт модулей вывода юнитов MYP и DP
import UnitMypList from "@/components/UnitMYPList";
import UnitDpList from "@/components/UnitDPList";
// Импорт модулей запросов базы подразделений, учителей
import { getDepartments } from "@/hooks/unit/getDepartments";
import { getTeachers } from "@/hooks/unit/getTeachers";

export default {
  name: 'UnitPlans',
  components: {
    UnitMypList, UnitDpList
  },
  setup(props) {
    const { departments } = getDepartments();
    const { teachers, getTeachersData } = getTeachers();
    return {
      departments, teachers, getTeachersData
    }
  },
  data() {
    return {

    }
  },
  methods: {
    
  },
  computed: {
    
  },
  mounted() {
    this.getTeachersData();
  },
}
</script>

<style scoped>

</style>