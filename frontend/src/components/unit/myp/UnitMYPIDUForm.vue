<template>
  <form id="unit-form">
    <!-- Поле для ввода названия юнита -->
    <div class="my-2">
      <label for="title" class="form-label">Название:</label>
      <input ref="title" id="title" class="form-control" type="text" v-model="editedUnit.title">
      <small ref="title_alert" class="alert-text"></small>
    </div>
    <div class="row my-2">
      <!-- Поле выбора года обучения  -->
      <div class="col-sm">
        <label for="grades" class="form-label">Год обучения:</label>
        <select ref="grade" id="grades" class="form-select" v-model="editedUnit.class_year_id" @change="getUnitsByYear">
          <option :value="null">Выберите год в MYP</option>
          <option v-for="(gr, i) in years" :key="i" :value="gr.id">
            {{ gr.year_rus }} класс ({{ gr.year_ib }})
          </option>
        </select>
        <small ref="year_alert" class="alert-text"></small>
      </div>
      <div class="col-sm-4">
        <label for="hours" class="form-label">Кол-во часов:</label>
        <input ref="hours" id="hours" class="form-control" type="number" v-model="editedUnit.hours">
        <small ref="hours_alert" class="alert-text"></small>
      </div>
    </div>
    <!-- Поле выбора критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценивания МДП: </div>
        <div v-if="criteriaMYP.length > 0">
          <div v-for="cr in criteriaMYP" :key="cr.id">
            <div class="form-check">
              <input ref="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id"
                v-model="editedUnit.criteria_ids">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}:</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Для выбора критериев оценки укажите дисциплину</div>
        <small ref="criteria_alert" class="alert-text"></small>
      </div>
    </div>
    <!-- Поле для выбора юнитов -->
    <div class="me-3 mb-2">Добавление юнитов в состав МДП: </div>
    <div class="border p-2">
      <div class="mb-1">
        <input id="authors" class="form-control" type="text" v-model="searchUnits"
          placeholder="Введите название юнита для поиска...">
      </div>
      <div v-if="searchUnitForIDU.length">
        <div v-for="(unit, index) in searchUnitForIDU.slice(0, 5)" :key="unit.id">
          <div class="form-check">
            <input ref="unit" class="form-check-input" type="checkbox" :value="unit.id" :id="'unit-' + unit.id"
              v-model="editedUnit.unitplan_myp_ids">
            <label class="form-check-label" :for="'unit-' + unit.id">
              <div>{{ unit.title }}</div>
              <div v-if="unit.subject">{{ unit.subject.name_rus }}</div>
            </label>
          </div>
          <div v-if="index == 4 && searchUnitForIDU.length != 5">...</div>
        </div>
      </div>
      <div v-else>Нет данных для отображения.<br>Выберите год обучения, чтобы получить список юнитов</div>
      <small ref="unitplan_myp_alert" class="alert-text"></small>
    </div>
  </form>
</template>
  
<script>
import { mapGetters } from 'vuex'
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";
import { getUnitListMYP } from "@/hooks/unit/useUnitMYP";

export default {
  props: {
    editedUnit: {
      type: Object,
      default: {
        criteria: {}
      }
    },
    validFormUnit: { type: Boolean },
  },
  setup(props) {
    const { years, fetchGetClassYears } = getClassYears();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();
    const { unitListMYP, fetchGetUnitListMYP } = getUnitListMYP();
    return {
      years, fetchGetClassYears,
      criteriaMYP, fetchGetCriteriaMYP,
      unitListMYP, fetchGetUnitListMYP,
    }
  },
  data() {
    return {
      textAlert: {
        title: 'Введите название юнита',
        unitplan_myp: 'Нужно выбрать 2 или более юнитов',
        year: 'Выберите год обучения',
        hours: 'Введите часы',
        criteria: 'Выберите критерии оценки',
      },
      errorField: {},
      searchUnits: '',
    }
  },
  methods: {
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.editedUnit.title ? this.errorField.title = false : this.errorField.title = true;
      this.editedUnit.unitplan_myp_ids.length >= 2 ? this.errorField.unitplan_myp = false : this.errorField.unitplan_myp = true;
      this.editedUnit.class_year_id ? this.errorField.year = false : this.errorField.year = true;
      this.editedUnit.hours ? this.errorField.hours = false : this.errorField.hours = true;
      this.editedUnit.criteria_ids.length ? this.errorField.criteria = false : this.errorField.criteria = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('update:validFormUnit', validate);
      this.validateForm();
    },
    // Валидация формы - проверка ошибок полей формы и вывод их в виде текста на форму
    validateForm() {
      for (let key in this.errorField) {
        if (this.$refs[`${key}_alert`]) {
          if (this.errorField[key]) {
            this.$refs[`${key}_alert`].innerText = this.textAlert[key];
          } else {
            this.$refs[`${key}_alert`].innerText = "";
          }
        }
      }
    },
    getUnitsByYear() {
      if (this.editedUnit.class_year_id) {
        this.fetchGetUnitListMYP({ year: this.editedUnit.class_year_id, interdisciplinary: 'no' })
      } else {
        this.unitListMYP = []
      }
    },
  },
  computed: {
    searchUnitForIDU() {
      if (!this.searchUnits) {
        return this.unitListMYP.filter((item, index) => {
          return (index < 5) || this.editedUnit.unitplan_myp_ids.includes(item.id)
        })
      }
      return this.unitListMYP.filter((item) => { 
        return item.title.toLowerCase().includes(this.searchUnits.toLowerCase()) || this.editedUnit.unitplan_myp_ids.includes(item.id)
      })
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    console.log('Форма создания юнита МДП инициализирована!');
    this.fetchGetClassYears({ program: 'MYP' });
    this.fetchGetCriteriaMYP({ group: 10 })
  },
}
</script>
  
<style scoped>
@import '@/assets/css/unitview.css';

.alert-text {
  color: red;
}

.alert-field {
  border-color: red;
}
</style>