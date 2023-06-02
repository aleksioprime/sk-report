<template>
  <div>
    <base-header>
      <template v-slot:link><a href="#" @click="$router.push(`/assessment/group`)" >Вернуться к выбору класса</a></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
    <div class="row ">
      <div class="col-md mb-2">
        <div>Период: <b>{{ currentPeriod.number }} {{ currentPeriod.type }}</b></div>
        <div>Класс: <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> ({{ getWordStudent(currentGroup.count) }}) 
        <br>Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }}
      </div>
        <div>Предмет: <b>{{ currentSubject.name_rus }} ({{ currentSubject.group_ib.name_eng }})</b></div>
      </div>
      <div v-if="authenticatedDnevnik" class="col-md data-dnevnik">
        <div class="dnevnik-biglogo" href="https://dnevnik.ru/"></div>
        <div>Вы успешно синхронизированы</div>
      </div>
      <div v-else class="col-md data-dnevnik">
        <div>
          Вы не синхронизированы с <a href="https://dnevnik.ru/">Дневник.ру</a>.<br>
          Для синхронизации авторизуйтесь в системе!
        </div> 
        <button class="btn btn-warning mt-2" @click="getDataDnevnik">Авторизоваться в Дневник.ру</button>
      </div>
    </div>
    <div>Выполненные итоговые работы за период</div>
    <div class="d-flex flex-column border p-2" v-if="summativeWorks.length">
      <div v-for="(worksByUnit, unit) in groupedArrayData(summativeWorks, ['unit'])" :key="unit.id">
        <b>{{ worksByUnit[0].unit.title }}</b>
        <div v-for="work in worksByUnit" :key="work.id">
          - {{ work.title }} (<span class="list-criteria" v-for="cr in work.criteria" :key="cr.id">{{ cr.letter }} </span>)
        </div>
      </div>
    </div>
    <div class="border p-2" v-else>
      За <b>{{ currentPeriod.number }} {{ currentPeriod.type }}</b> в <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> классе итоговых работ не проводилось!
    </div>
    <div v-if="!isStudentsAssessmentLoading || !firstLoading">
      <table class="asessment-table table table-sm table-bordered mt-2 table-responsive w-100">
        <thead class="text-center align-middle">
          <tr>
            <th scope="col" rowspan="2">№</th>
            <td scope="col" rowspan="2">ФИО студента</td>
            <td scope="col" colspan="6">Оценка за итоговые работы</td>
            <td rowspan="2" style="width: 25px">Среднее текущее</td>
            <td rowspan="2" style="width: 25px">Итог</td>
          </tr>
          <tr>
            <td class="column-criteria">A</td>
            <td class="column-criteria">B</td>
            <td class="column-criteria">C</td>
            <td class="column-criteria">D</td>
            <td class="column-criteria">Сумма</td>
            <td style="width: 25px">Итог</td>
          </tr>
        </thead>
        <tbody>
          <template v-for="(st, index) in studentsAssessment" :key="st.id">
            <tr>
              <th scope="row" rowspan="2">{{ index + 1 }}</th>
              <td rowspan="2">{{ st.user.last_name }} {{ st.user.first_name }}</td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-a" v-for="mark in st.criteria_list.criteria_a" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-b" v-for="mark in st.criteria_list.criteria_b" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-c" v-for="mark in st.criteria_list.criteria_c" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-d" v-for="mark in st.criteria_list.criteria_d" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable">
                <div v-if="st.criteria_num">{{ st.criteria_sum }}/{{ st.criteria_num * 8 }}</div>
              </td>
              <td class="uneditable">{{ st.criteria_result }}</td>
              <td class="uneditable">
                <div class="dnevnik-mark">
                  <div class="dnevnik-smalllogo"></div>
                  <div v-if="isDataDnevnikLoading">
                    {{ marksDnevnik.marks[st.id_dnevnik] }}
                  </div>
                  <div v-else class="loader-mark">
                    
                  </div>
                </div>
              </td>
              <td class="uneditable">
                <div v-if="st.criteria_result && marksDnevnik.marks[st.id_dnevnik]">
                  {{ getFinalGrade(marksDnevnik.marks[st.id_dnevnik], st.criteria_result) }}
                </div>
              </td>
            </tr>
            <tr>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_a">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_a || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_b">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_b || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_c">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_c || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_d">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_d || '-' }}</div>
              </td>
              <td class="uneditable" :title="st.periodassess.prediction_criterion">
                <div v-if="st.periodassess.count_criterion">{{ st.periodassess.summ_criterion }}/{{ st.periodassess.count_criterion * 8 }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.summ_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.summ_grade || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.form_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.form_grade || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.final_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.final_grade || '-' }}</div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
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
import { updateUser } from "@/hooks/user/useUser";
import { mapGetters } from 'vuex';
import { getAssessmentJournal, getSummativeWork, getStudentsAssessment, getAssessmentDnevnik } from "@/hooks/assess/usePeriodAssessment";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

const CLIEND_ID = '3097117bc2af450db4de47abe50d22ba'


export default {
  name: 'AssessPeriodView',
  components: {

  },
  setup(props) {
    const { studentsAssessment, isStudentsAssessmentLoading, fetchGetStudentsAssessment } = getStudentsAssessment();
    const { summativeWorks, fetchGetSummativeWork } = getSummativeWork();
    const { groupedArrayData } = getGroupedArray();
    const { currentPeriod, currentSubject, currentGroup, fetchGetAssessmentJournal } = getAssessmentJournal();
    const { fetchUpdateUser } = updateUser();
    const { marksDnevnik, isDataDnevnikLoading, fetchGetAssessmentDnevnik } = getAssessmentDnevnik();
    return {
      studentsAssessment, isStudentsAssessmentLoading, fetchGetStudentsAssessment,
      summativeWorks, fetchGetSummativeWork,
      groupedArrayData,
      currentPeriod, currentSubject, currentGroup, fetchGetAssessmentJournal,
      fetchUpdateUser,
      marksDnevnik, isDataDnevnikLoading, fetchGetAssessmentDnevnik,
    }
  },
  data() {
    return {
      currentAssess: {},
      firstLoading: true,
      authenticatedDnevnik: false,
    }
  },
  methods: {
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    getFinalGrade(formGrade, sumGrade) {
      return +(formGrade * 0.4 + sumGrade * 0.6).toFixed(2)
    },
    setEditField(event, student) {
      let textElement = event.target
      let inputElement = event.target.parentElement.firstChild
      inputElement.value = textElement.textContent
      textElement.style.display = 'none';
      inputElement.style.display = 'block';
      inputElement.focus();
      inputElement.select();
      // Функция для сохранения изменённых данных в ячейке
      const saveData = () => {
        if (student.periodassess.id) {
          this.setStudentGradeEdit(student.periodassess.id);
        } else {
          this.setStudentGradeAdd(student.id);
        }
        textElement.textContent = inputElement.value;
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
      }
      // Функция для отмены сохранения изменённых данных в ячейке
      const cancelData = () => {
        console.log('Отмена редактирования');
        inputElement.onblur = null;
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
        this.currentAssess = {};
      }
      // Привязка функций к событиям потери фокуса и нажатию на Enter
      inputElement.onblur = saveData;
      inputElement.onkeypress = (e) => {
        if (e.key === "Enter") { saveData() } 
        else if (e.key === "Escape") { cancelData() }
      };
    },
    setStudentGradeEdit(periodassess_id) {
      if (Object.keys(this.currentAssess).length) {
        console.log("Запрос на изменение данных: ", this.currentAssess);
        this.axios.put(`/assessment/periodassess/${periodassess_id}`, this.currentAssess).then((response) => {
          console.log('Оценка успешно изменена', response.data);
          const index = this.studentsAssessment.findIndex(item => item.periodassess.id == periodassess_id);
          if (index != -1) {
            this.studentsAssessment[index].periodassess = response.data
          }
          // this.fetchGetStudentsAssessment({
          //   group: this.$route.params.id_group, 
          //   period: this.$route.params.id_period,
          //   subject: this.$route.params.id_subject,
          //   class_year: this.currentGroup.class_year.id,
          // });
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
    setStudentGradeAdd(student_id) {
      if (Object.keys(this.currentAssess).length) {
        this.currentAssess.student_id = student_id;
        this.currentAssess.subject_id = this.$route.params.id_subject;
        this.currentAssess.period_id = this.$route.params.id_period;
        this.currentAssess.year_id = this.currentGroup.class_year.id;
        console.log("Запрос на Добавление данных: ", this.currentAssess);
        this.axios.post(`/assessment/periodassess`, this.currentAssess).then((response) => {
          console.log('Оценка успешно добавлена', response.data);
          this.fetchGetStudentsAssessment({
            group: this.$route.params.id_group, 
            period: this.$route.params.id_period,
            subject: this.$route.params.id_subject,
            class_year: this.currentGroup.class_year.id,
          });
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
    getDataDnevnik() {
      window.location.href = `https://login.dnevnik.ru/oauth2?response_type=token&client_id=${CLIEND_ID}&scope=CommonInfo,ContactInfo,EducationalInfo&redirect_uri=${window.location.href}&state=`;
    },
    getValueFromHash(hash) {
      return  hash.split('&').reduce(function (res, item) {
        var parts = item.split('=');
        res[parts[0]] = parts[1];
        return res;
      }, {});
    },
  },
  mounted() {
    if (this.authUser.access_token_dnevnik) {
      this.authenticatedDnevnik = true
    }
    if (this.$route.hash) {
      if (this.getValueFromHash(this.$route.hash.slice(1)).access_token != this.authUser.access_token_dnevnik) {
        console.log('Получен новый токен');
        let updateUser = {
          id: this.authUser.id,
          username: this.authUser.username,
          first_name: this.authUser.first_name,
          last_name: this.authUser.last_name,
          email: this.authUser.email,
          access_token_dnevnik: this.getValueFromHash(this.$route.hash.slice(1)).access_token,
        }
        this.fetchUpdateUser(updateUser).finally(() => {
          this.$router.push(this.$route.path)
        })
      } else {
        console.log('Получен старый токен');
        this.$router.push(this.$route.path)
      }
    } else {
      console.log('Токенов не приходило')
    }
    this.fetchGetAssessmentJournal({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
    }).finally(() => {
      this.fetchGetAssessmentDnevnik({
        group_dnevnik: this.currentGroup.id_dnevnik, 
        period_dnevnik: this.currentPeriod.id_dnevnik,
        subject_dnevnik: this.currentSubject.id_dnevnik,
        user: this.authUser.id
      }).finally(() => {
        if (this.marksDnevnik.result) {
          this.authenticatedDnevnik = true
        } else {
          this.authenticatedDnevnik = false
        }
      })
    })
    this.fetchGetSummativeWork({
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
      group: this.$route.params.id_group,
      teacher: this.authUser.teacher.id
    });
    this.fetchGetStudentsAssessment({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
      class_year: this.currentGroup.class_year.id,
    }).finally(() => {
      this.firstLoading = false;
    });

  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser']),
  },
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';
.loader {
  display: flex;
  height: calc(100vh - 200px);
  align-items: center;
  justify-content: center;
}
.link-back {
  cursor: pointer;
}
.asessment-table th {
  text-align: center;
}
.column-criteria {
  min-width: 50px;
}
.data-dnevnik {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 70px;
  border: 1px solid #dee2e6;
  padding: 10px;
  text-align: center;
  margin-bottom: 10px;
}
.dnevnik-biglogo {
  width: 143px;
  height: 50px;
  background: url('@/assets/img/dnevnik.svg') no-repeat 50% / 90%;
  margin-right: 10px;
}
.dnevnik-mark {
  position: relative;
  min-height: 24px;
  color: #0273B2;
  font-weight: 700;
}
.dnevnik-smalllogo {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  background: url('@/assets/img/dnevnik_small.svg') no-repeat 50% / 90%;
}
.criterion-mark {
  display: flex;
}
.criterion-mark.item {
  padding: 3px;
  border-radius: 3px;
}
.item.cr-a{
  background: #c7735e;
  color: #fff;
}
.item.cr-b{
  background: #c7c55e;
  color: #fff;
}
.item.cr-c{
  background: #2cb801;
  color: #fff;
}
.item.cr-d{
  background: #ae5ec7;
  color: #fff;
}
.criterion-mark.item:not(:last-of-type) {
  margin-right: 3px;
}
.list-criteria {
  font-weight: 700;
}.list-criteria:not(:last-of-type)::after {
  content: ', '
}
.caption {
  margin-bottom: 10px;
  font-size: 18px;
}

.info-block {
  margin: 10px 0px 0px;
}

.table-input {
  border: none;
  display: none;
  width: 25px;
}
.table-text {
  cursor: pointer;
}
table .uneditable {
  background-color: #f7f7f7;
  vertical-align: middle;
  text-align: center;
  min-width: 20px;
}
table .editable {
  background-color: #ffffff;
  font-weight: 500;
  text-align: center;
  min-width: 20px;
  /* cursor: pointer; */
}
/* table .editable:hover {
  background-color: #fffcfc;
} */

.loader-mark {
  width: 16px;
  height: 16px;
  border: 5px solid #0273B2;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
  }

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
} 
</style>