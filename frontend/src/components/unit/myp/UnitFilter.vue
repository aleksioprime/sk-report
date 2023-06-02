<template>
  <div class="block-filter">
    <div v-if="showAllUnits">
      <div class="block-departments">
        <div v-for="dp in departments" :key="dp.id" class="department radiobutton">
          <input type="radio" name="department" :value="dp.id" :id="'department-' + dp.id"
            v-model="queryDepartment" @change="changeDepartment">
          <label :for="'department-' + dp.id">
            <div class="img"><img :src='dp.photo ? dp.photo : require("@/assets/img/sk_report_logo_notext.svg")' alt="" width="50" height="50"></div>
            <div>{{ dp.name }}</div>
          </label>
        </div>
      </div>
    </div>
    <div class="block-subject">
      <div class="subject radiobutton">
        <input type="radio" name="subject" :value="null" :id="'subject-x'" v-model="querySubject"
          @change="changeSubject">
        <label :for="'subject-x'">
          Все предметы
        </label>
      </div>
      <div v-for="sb in subjects" :key="sb.id" class="subject radiobutton">
        <input type="radio" name="subject" :value="sb.id" :id="'subject-' + sb.id"
          v-model="querySubject" @change="changeSubject">
        <label :for="'subject-' + sb.id">
          {{ sb.name_rus }}
        </label>
      </div>
    </div>
    <div class="d-flex align-items-center year-filter" v-if="years.length > 0" :class="{ 'filter-active' : this.queryYears.length }">
      <div class="me-2" v-for="year in years" :key="year.id">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" :value="year.id" :id="'year-' + year.id" v-model="queryYears"
            @change="handleQuery">
          <label class="form-check-label" :for="'year-' + year.id">
            <span v-if="year.id">{{ year.year_ib }}</span>
          </label>
        </div>
      </div>
      <!-- <div v-if="this.queryYears.length == 0" class="ms-auto">Показаны юниты всех лет</div>
      <div v-else class="ms-auto">Показан юниты выбранных лет</div> -->
    </div>
  </div>
</template>

<script>
import { getDepartments } from "@/hooks/user/useDepartment";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getSubjects } from "@/hooks/curriculum/useSubject";

export default {
  props: {
    showAllUnits: {
      type: Boolean,
      default: false,
    },
    user: {
      type: Object
    },
  },
  setup(props) {
    const { departments, fetchGetDepartments } = getDepartments();
    const { years, fetchGetClassYears } = getClassYears();
    const { subjects, fetchGetSubjects } = getSubjects();

    return {
      departments, fetchGetDepartments,
      years, fetchGetClassYears,
      subjects, fetchGetSubjects,
    }
  },
  data() {
    return {
      querySubject: null,
      queryYears: [],
      queryDepartment: null,
    }
  },
  methods: {
    handleQuery(event) {
      this.$emit('updateFetch', { years: this.queryYears, subject: this.querySubject, department: this.queryDepartment });
    },
    changeDepartment() {
      this.querySubject = null;
      if (this.showAllUnits) {
        this.fetchGetSubjects({ department: this.queryDepartment, program: 'MYP' }).finally(() => {
          this.changeSubject();
        });
      } else {
        this.fetchGetSubjects({ author: this.user.teacher.id, program: 'MYP' }).finally(() => {
          this.changeSubject();
        }); 
      }
    },
    changeSubject() {
      this.queryYears = [];
      if (this.showAllUnits) {
        if (this.querySubject) {
          this.fetchGetClassYears({ subject: this.querySubject, program: 'MYP' }).finally(() => {
          this.handleQuery();
        });
        } else {
          this.fetchGetClassYears({ department: this.queryDepartment, program: 'MYP' }).finally(() => {
          this.handleQuery();
        });
        }
      } else {
        this.fetchGetClassYears({ author: this.user.teacher.id, subject: this.querySubject, program: 'MYP' }).finally(() => {
          this.handleQuery();
        });
      }
    },
    fetchAllDataForUnits() {
      if (this.showAllUnits) {
        console.log('Включён режим администратора');
        this.fetchGetDepartments().finally(() => {
          if (this.departments.length) {
            this.queryDepartment = this.departments[0].id;
          }
          this.querySubject = null;
          this.queryYears = [];
          this.fetchGetClassYears({ department: this.queryDepartment, program: 'MYP' });
          this.fetchGetSubjects({ department: this.queryDepartment, program: 'MYP' }).finally(() => {
            this.handleQuery();
          }); 
        });
      } else {
        console.log('Режим администратора выключен');
        this.queryDepartment = null;
        this.querySubject = null;
        this.queryYears = [];
        this.fetchGetSubjects({ author: this.user.teacher.id, program: 'MYP' }).finally(() => {
          this.fetchGetClassYears({ author: this.user.teacher.id, program: 'MYP' }).finally(() => {
            this.handleQuery();
          });
        });
      }
    }
  },
  mounted() {
  },
  watch: {
    showAllUnits() {
      this.fetchAllDataForUnits();
    }
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
}
.block-departments {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 5px;
  margin-bottom: 10px;
}
.department {
	flex-basis: 10%;
  flex-grow: 1;
  min-width: 50px;
}
@media (max-width: 1200px) {
  .department {
    flex-basis: 18%;
  }
  /* .department:last-of-type {
    flex-grow: 0;
  } */
}
.department img {
  margin-bottom: 10px;
  object-fit: contain;
}
.block-subject {
  display: flex;
  flex-wrap: wrap;
  /* flex-direction: column; */
  gap: 5px;
  margin-bottom: 10px;
}
.year-filter {
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding: 10px;
}
.filter-active {
  
  border: 1px solid var(--bs-primary);
}
</style>