<template>
  <div>
    <base-header>
      <template v-slot:header>Список юнитов</template>
    </base-header>
    <transition name="fade">
      <div v-show="showMYPData">
        <ul class="nav nav-tabs mb-3" id="pills-tab" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" id="pills-myp-tab" data-bs-toggle="pill" data-bs-target="#pills-myp" type="button" role="tab" aria-controls="pills-myp" aria-selected="true">Программа средней школы (MYP)</button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="pills-dp-tab" data-bs-toggle="pill" data-bs-target="#pills-dp" type="button" role="tab" aria-controls="pills-dp" aria-selected="false">Программа старшей школы (DP)</button>
          </li>
        </ul>
        <div class="tab-content" id="pills-tabContent">
          <div class="tab-pane fade show active" id="pills-myp" role="tabpanel" aria-labelledby="pills-myp-tab">
            <unit-myp-list :departments="departments" @showMYPData="showMYPData = true"/>
          </div>
          <div class="tab-pane fade" id="pills-dp" role="tabpanel" aria-labelledby="pills-dp-tab">
            <!-- <unit-dp-list :departments="departments"/> -->
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
// Импорт модулей вывода юнитов MYP и DP
import UnitMypList from "@/components/UnitMYPList";
import UnitDpList from "@/components/UnitDPList";
// Импорт модулей запросов базы подразделений, учителей
import { getDepartments } from "@/hooks/unit/getUnitData"

export default {
  name: 'UnitPlans',
  components: {
    UnitMypList, UnitDpList
  },
  setup(props) {
    const { departments, getDepartmentsData } = getDepartments();
    return {
      departments, getDepartmentsData
    }
  },
  data() {
    return {
      showMYPData: false,
    }
  },
  methods: {
    
  },
  computed: {
    
  },
  mounted() {
    this.getDepartmentsData();
  },
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.nav-link.active {
  background-color: #ffffff !important;
  color: #495057;
}
</style>