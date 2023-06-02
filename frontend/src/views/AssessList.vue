<template>
  <div>
    <base-header>
      <template v-slot:header>Мои итоговые работы</template>
    </base-header>
    <button type="button" class="btn btn-primary" @click="showSumWorkModalAdd">
      Cоздать итоговую работу
    </button>
    <assessment-filter @updateFetch="updateFetch" :studyPrograms="studyPrograms"/>
    <!-- Модальное окно добавления/редактирования/удаления итоговой работы -->
    <modal-assess :modalTitle="modalTitle" :flagAssess="flagAssess" 
      @create="sumWorkCreate" @delete="sumWorkDelete" @update="sumWorkEdit" @cancel="hideSumWorkModal">
      <template v-slot:body>
        <!-- Форма добавления/редактирования итоговой работы -->
        <assessment-form v-model:summativeWork="currentAssess" v-if="flagAssess.add || flagAssess.edit"
        :studyPrograms="studyPrograms" @validForm="validFormResult" ref="assessmentForm" :editMode="formEditMode"/>
        <!-- Текст удаления итоговой работы -->
        <div v-if="flagAssess.delete" >
          <div class="mb-2">Вы действительно хотите удалить эту итоговую работу?</div>
          <div class="border p-2">
            <h4>{{ currentAssess.title }}</h4>
            <div>{{ currentAssess.unit.title }}</div>
            <div v-for="gr in currentAssess.groups" :key="gr.id">{{ gr.group.class_year.year_rus }}{{ gr.group.letter }} класс - {{ new Date(gr.date).toLocaleDateString() }}</div>
          </div>
        </div>
      </template>
    </modal-assess>
    
    <!-- Вывод итоговых работ учителя, сгруппированных по предметам -->
    <div v-if="Object.keys(groupedArrayData(summativeWorks, ['subject', 'id'])).length !== 0" class="sumworks">
      <div v-for="(worksBySubject, subject) in groupedArrayData(summativeWorks, ['subject', 'id'])" :key="subject">
        <div class="sumworks-subject" v-if="getSubject(subject)"><h3>{{ getSubject(subject).name_rus }}</h3></div>
        <div v-for="(worksByYear, year) in groupedArrayData(worksBySubject, ['unit', 'class_year', 'year_rus'])" :key="year" class="sumworks-block area">
          <div class="sumworks-year">
            <div class="title" v-if="year"><h4>{{ year }} классы</h4></div>
          </div>
          <div class="sumworks-grouped">
            <assessment-item v-for="sumwork in worksByYear" :key="sumwork.id" :sumwork="sumwork" @editWork="showSumWorkModalEdit(sumwork.id)" @deleteWork="showSumWorkModalDelete(sumwork.id)"/>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="sumworks-empty">
      Нет данных
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';
import AssessmentForm from "@/components/assessment/AssessmentForm.vue";
import AssessmentItem from "@/components/assessment/AssessmentItem.vue";
import AssessmentFilter from "@/components/assessment/AssessmentFilter.vue";
import { getSummativeWorks, createSummativeWork, updateSummativeWork, deleteSummativeWork } from "@/hooks/assess/useSummativeWork";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'Assessment',
  components: {
    AssessmentForm, AssessmentItem, AssessmentFilter
  },
  setup(props) {
    const { summativeWorks, isSumWorkLoading, fetchGetSummativeWorks } = getSummativeWorks();
    const { createdSummativeWork, fetchCreateSummativeWork } = createSummativeWork();
    const { updatedSummativeWork, fetchUpdateSummativeWork } = updateSummativeWork();
    const { fetchDeleteSummativeWork } = deleteSummativeWork();
    const { groupedArrayData } = getGroupedArray();

    return {
      summativeWorks, isSumWorkLoading, fetchGetSummativeWorks,
      createdSummativeWork, fetchCreateSummativeWork,
      updatedSummativeWork, fetchUpdateSummativeWork,
      fetchDeleteSummativeWork,
      groupedArrayData
    }
  },
  data() {
    return {
      currentPeriod: null,
      modalAssess: {},
      modalTitle: '',
      flagAssess: {},
      currentAssess: {
        teacher_id: null,
        criteria_ids: [],
        groups: [],
        subject_id: null,
        unit_id: null,
        period_id: null,
      },
      validForm: false,
      formEditMode: false,
      studyPrograms: [
        { value: 'PYP', name_eng: 'Primary Years Programme', name_rus: 'Программа начальной школы' },
        { value: 'MYP', name_eng: 'Middle Years Programme', name_rus: 'Программа средней школы' },
        { value: 'DP', name_eng: 'Diploma Programme', name_rus: 'Программа старшей школы DP' },
        { value: 'FGOS', name_eng: 'ФГОС', name_rus: 'Программа старшей школы ФГОС' },
      ]
    }
  },
  methods: {
    updateFetch(data) {
      this.currentPeriod = data.period;
      console.log('Параметры фильтрации: ', data)
      this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
    },
    hideSumWorkModal() {
      this.modalAssess.hide();
      this.flagAssess = {}
      this.currentAssess = {
          teacher_id: null,
          criteria_ids: [],
          groups: [],
          subject_id: null,
          unit_id: null,
          period_id: null,
        };
    },
    showSumWorkModalAdd() {
      this.modalTitle = 'Создание итоговой работы';
      this.formEditMode = false;
      this.currentAssess.teacher_id = this.authUser.teacher.id;
      this.currentAssess.period_id = this.currentPeriod.id;
      this.modalAssess.show();
      this.flagAssess.add = true;
    },
    showSumWorkModalEdit(id) {
      this.modalTitle = 'Редактирование итоговой работы';
      this.formEditMode = true;
      this.currentAssess = { ...this.summativeWorks.find(item => item.id == id) };
      this.currentAssess.teacher_id = this.currentAssess.teacher.id;
      this.currentAssess.subject_id = this.currentAssess.subject.id;
      this.currentAssess.unit_id = this.currentAssess.unit.id;
      this.currentAssess.period_id = this.currentAssess.period.id;
      this.currentAssess.criteria_ids = this.currentAssess.criteria.map(item => item.id);
      this.currentAssess.groups = this.currentAssess.groups.map(item => {
        return {
          id: item.id,
          group_id: item.group.id,
          date: item.date,
          lesson: item.lesson,
        }
      })
      this.modalAssess.show();
      this.flagAssess.edit = true;
      
    },
    showSumWorkModalDelete(id) {
      this.modalTitle = 'Удаление итоговой работы';
      this.currentAssess = { ...this.summativeWorks.find(item => item.id == id) };
      this.modalAssess.show();
      this.flagAssess.delete = true;
    },
    // Получение результатов валидации из компонента с формой
    validFormResult(value) {
      this.validForm = value;
    },
    sumWorkCreate() {
      this.$refs.assessmentForm.checkFieldsValidate();
      if (this.validForm) {
        console.log("Запрос на создание итоговой работы: ", this.currentAssess);
        this.fetchCreateSummativeWork(this.currentAssess).finally(() => {
          this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
          this.hideSumWorkModal();
        })
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkEdit() {
      this.$refs.assessmentForm.checkFieldsValidate();
      if (this.validForm) {
        console.log("Запрос на изменение итоговой работы: ", this.currentAssess);
        this.fetchUpdateSummativeWork(this.currentAssess.id, this.currentAssess).finally(() => {
          this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
          this.hideSumWorkModal();
        });
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkDelete() {
      console.log("Запрос на удаление итоговой работы");
      this.fetchDeleteSummativeWork(this.currentAssess.id).finally(() => {
        this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
        this.hideSumWorkModal();
      });
    },
    // Нахождение предмета по его ID из списка итоговых работ
    getSubject(id) {
      let subject = null;
      this.summativeWorks.forEach((item) => {
        if (item.subject.id == id) {
          subject = item.subject
          return
        }
      })
      return subject
    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalAssess = new Modal('#modalAssess', { backdrop: 'static' });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>

<style>
.tools {
  display: flex;
  align-items: center;
}
.tools .btn {
  max-width: 300px;
}
.sumworks {
  display: flex;
  flex-direction: column;
  padding: 10px;
}
.sumworks-block {
  margin-top: 10px;
}
.sumworks-subject {
  margin-top: 10px;
  font-size: 2em;
  padding-bottom: 5px;
}
.sumworks-subject .title {
  font-weight: 700;
  text-transform: uppercase;
}
.sumworks-year {
  display: flex;
  align-items: center;
  padding: 10px;
}

.sumworks-year .title{
  color: var(--bs-secondary);
  font-weight: 700;
}
.sumworks-empty {
  display: flex;
  height: calc(100vh - 500px);
  align-items: center;
  justify-content: center;
}
</style>