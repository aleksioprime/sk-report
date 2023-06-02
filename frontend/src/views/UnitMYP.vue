<template>
  <div>
    <base-header>
      <template v-slot:header>
        <div>MYP: список <span v-if="showAllUnits">всех</span><span v-else>моих</span> юнитов</div>
      </template>
      <template v-slot:extra>
        <div class="toggle" v-if="isAdmin">
          <div class="toggle-item my">
            <input id="show-my" type="radio" :value="false" v-model="showAllUnits">
            <label for="show-my">Мои</label>
          </div>
          <div class="toggle-item all">
            <input id="show-all" type="radio" :value="true" v-model="showAllUnits">
            <label for="show-all">Все</label>
          </div>
        </div>
      </template>
    </base-header>
    <div class="row">
      <div class="col-md mb-2">
        <button type="button" class="btn btn-primary" @click="showAddUnit">
          Cоздать юнит
        </button>
        <button type="button" class="btn btn-primary" @click="showAddIDU">
          Cоздать МДП
        </button>
      </div>
    </div>
    <!-- Инструменты фильтрации юнитов -->
    <unit-filter ref="unitFilter" :showAllUnits="showAllUnits" :user="authUser" @updateFetch="getFilters"/>
    <!-- Список юнитов -->
    <div v-if="!isUnitLoading || !firstLoading" class="mt-3">
      <unit-myp-list :units="unitsMYP" @changePage="changePage" :totalPages="totalPages" :currentPage="currentPage" />
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
    <!-- Модальное окно с формой добавления юнита -->
    <modal-unit :modalId="'modalUnit'" :modalTitle="modalTitle" :flagUnit="flagUnit" @cancel="hideUnitModal" @create="unitCreate">
      <unit-myp-form v-if="flagUnit.add" ref="formUnit" v-model:editedUnit="editedUnit" v-model:validFormUnit="validFormUnit"/>
      <div v-if="flagUnit.delete">
        <div>Вы действительно хотите удалить этот юнит?</div>
        <div>
          <div>{{ editedUnit.title }}</div>
        </div>
      </div>
    </modal-unit>
    <!-- Модальное окно с формой добавления МДП -->
    <modal-unit :modalId="'modalUnitIDU'" :modalTitle="modalTitle" :flagUnit="flagUnitIDU" @cancel="hideUnitIDUModal" @create="unitIDUCreate">
      <unit-myp-idu-form v-if="flagUnitIDU.add" ref="formUnitIDU" v-model:editedUnit="editedUnitIDU" v-model:validFormUnit="validFormUnitIDU"/>
    </modal-unit>
  </div>
</template>
  
<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';
import UnitMypList from "@/components/unit/myp/UnitMYPList";
import UnitFilter from "@/components/unit/myp/UnitFilter";
import UnitMypForm from "@/components/unit/myp/UnitMYPForm";
import UnitMypIduForm from "@/components/unit/myp/UnitMYPIDUForm";

import { getUnitsMYP, createUnitMYP } from "@/hooks/unit/useUnitMYP";
import { createInterdisciplinaryUnit } from "@/hooks/unit/useInterdisciplinaryUnit";

export default {
  name: 'UnitMYP',
  components: {
    UnitMypList, UnitFilter, UnitMypForm, UnitMypIduForm
  },
  setup(props) {
    const { unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP } = getUnitsMYP();
    const { createdUnitMYP, fetchCreateUnitMYP } = createUnitMYP();
    const { interdisciplinaryUnit, fetchCreateInterdisciplinaryUnit } = createInterdisciplinaryUnit();
    return {
      unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP,
      createdUnitMYP, fetchCreateUnitMYP,
      interdisciplinaryUnit, fetchCreateInterdisciplinaryUnit,
    }
  },
  data() {
    return {
      currentPage: 1,
      limit: 15,
      flagUnit: {},
      flagUnitIDU: {},
      validFormUnit: false,
      validFormUnitIDU: false,
      editedUnit: {},
      editedUnitIDU: {},
      modalTitle: null,
      showAllUnits: false,
      currentFilter: {
        department: null,
        subject: null,
        years: []
      },
      firstLoading: true,
    }
  },
  methods: {
    // Выбор текущей страницы
    changePage(page) {
      this.currentPage = page;
      if (this.showAllUnits) {
        this.fetchGetUnitsMYP({ department: this.currentFilter.department, years: this.currentFilter.years, subject: this.currentFilter.subject, page: this.currentPage, limit: this.limit });   
      } else {
        this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, years: this.currentFilter.years, subject: this.currentFilter.subject, page: this.currentPage, limit: this.limit });
      }
    },
    // Открытие модального окна для добавления юнита 
    showAddUnit() {
      this.modalTitle = "Создание юнита MYP";
      this.flagUnit.add = true;
      this.editedUnit = {
        class_year_id: null,
        subject_id: null,
        level_id: null,
        authors_ids: [],
        criteria_ids: [],
      };
      this.modalUnit.show();
    },
    // Открытие модального окна для удаления юнита 
    showDelUnit(unit) {
      this.modalTitle = "Удаление юнита MYP";
      this.editedUnit = unit;
      this.flagUnit.delete = true;
      this.modalUnit.show();
    },
    // Закрытие модального окна
    hideUnitModal() {
      this.validFormUnit = false;
      this.editedUnit = {};
      this.modalUnit.hide();
      this.flagUnit = {};
    },
    // Создание юнита (отправка post запроса на сервер)
    unitCreate() {
      this.$refs.formUnit.checkFieldsValidate();
      if (this.validFormUnit) {
        console.log("Запрос на создание юнита: ", this.editedUnit);
        this.fetchCreateUnitMYP(this.editedUnit).then(() => {
          this.$refs.unitFilter.fetchAllDataForUnits();
          this.updateFetchUnitMYP();
          this.hideUnitModal();
        })
      } else {
        console.log('Валидация неуспешна', this.editedUnit)
      }
    },
    getFilters(data) {
      console.log('Выбранные фильтры: ', data)
      this.currentFilter.department = data.department;
      this.currentFilter.subject = data.subject;
      this.currentFilter.years = data.years;
      this.updateFetchUnitMYP();
    },
    //
    updateFetchUnitMYP() {
      if (this.showAllUnits) {
        this.fetchGetUnitsMYP({ department: this.currentFilter.department, years: this.currentFilter.years, subject: this.currentFilter.subject, limit: this.limit });   
      } else {
        this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, years: this.currentFilter.years, subject: this.currentFilter.subject, limit: this.limit });
      }
    },
    showAddIDU() {
      this.modalTitle = "Создание междисциплинарного юнита MYP";
      this.editedUnitIDU = {
        class_year_id: null,
        criteria_ids: [],
        unitplan_myp_ids: [],
      };
      this.flagUnitIDU.add = true;
      this.modalUnitIDU.show();
    },
    hideUnitIDUModal() {
      this.modalUnitIDU.hide();
    },
    unitIDUCreate() {
      this.$refs.formUnitIDU.checkFieldsValidate();
      if (this.validFormUnitIDU) {
        console.log("Запрос на создание юнита: ", this.editedUnitIDU);
        this.fetchCreateInterdisciplinaryUnit(this.editedUnitIDU).finally(() => {
          this.$refs.unitFilter.fetchAllDataForUnits();
          this.updateFetchUnitMYP();
          this.hideUnitIDUModal();
        })
      } else {
        console.log('Валидация неуспешна', this.editedUnitIDU)
      }
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    // Определение модального окна для создания юнита
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    this.modalUnitIDU = new Modal('#modalUnitIDU', { backdrop: 'static' });
    if (this.isAdmin) {
      this.showAllUnits = true;
    } else {
      this.$refs.unitFilter.fetchAllDataForUnits();
    }
  },
}
</script>
  
<style scoped>
@import '@/assets/css/spinner.css';
</style>