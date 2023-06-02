<template>
  <div class="form-edit">
    <div class="form-title">
      <span v-if="deletionMode">Удаление предмета</span>
      <span v-else-if="editableData.id">Редактирование предмета</span>
      <span v-else>Добавление предмета</span>
    </div>
    <div v-if="deletionMode">Вы действительно хотите удалить этот предмет?</div>
    <div v-else>
      <div class="row">
        <div class="col-md">
          <input v-model="editableData.name_rus" type="text" placeholder="Название на рус.языке" class="form-control my-1">
        </div>
        <div class="col-md">
          <input v-model="editableData.name_eng" type="text" placeholder="Название на англ.языке" class="form-control my-1">
        </div>
      </div>
      <div class="row">
        <div class="col-md">
          <select id="class_year" class="form-select my-1" v-model="editableData.level">
            <option :value="null">Выберите уровень</option>
            <option v-for="lvl in levels" :key="lvl.value" :value="lvl.value">
              {{ lvl.name }} 
            </option>
          </select>
        </div>
        <div class="col-md-5">
          <select id="class_year" class="form-select my-1" v-model="editableData.type">
            <option :value="null">Выберите тип</option>
            <option v-for="tp in types" :key="tp.value" :value="tp.value">
              {{ tp.name }} 
            </option>
          </select>
        </div>
        <div class="col-md">
          <input v-model="editableData.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
        </div>
      </div>
      <div class="row">
        <div class="col-md">
          <select id="class_year" class="form-select my-1" v-model="editableData.group_ib_id">
            <option :value="null">Выберите IB-группу</option>
            <option v-for="ib in ib_groups" :key="ib.id" :value="ib.id">
              {{ ib.name_eng }} 
            </option>
          </select>
        </div>
        <div class="col-md">
          <select id="class_year" class="form-select my-1" v-model="editableData.group_fgos_id">
            <option :value="null">Выберите ФГОС-группу</option>
            <option v-for="fgos in fgos_groups" :key="fgos.id" :value="fgos.id">
              {{ fgos.name_rus }} ({{ fgos.type }})
            </option>
          </select>
        </div>
        <div class="col-md">
          <select id="class_year" class="form-select my-1" v-model="editableData.department_id">
            <option :value="null">Выберите подразделение</option>
            <option v-for="dp in departments" :key="dp.id" :value="dp.id">
              {{ dp.name }}
            </option>
          </select>
        </div>
      </div>
      <div>
        <div class="form-check mt-2">
          <input class="form-check-input" type="checkbox" id="report" v-model="editableData.need_report">
          <label class="form-check-label" for="report">Предмет поддерживает репорты</label>
        </div>
      </div>
    </div>
    
    <div class="d-flex mt-2 justify-content-end">
      <button class="btn btn-success" @click="$emit('apply', this.editableData)">ОК</button>
      <button class="btn btn-cancel" @click="$emit('cancel')">Отмена</button>
    </div>
  </div>
</template>
  
<script>

export default {
  name: 'SubjectForm',
  props: {
    editableData: { type: Object, default: {
      subject_id: null,
      group_id: null,
      teacher_id: null,
    } },
    departments: { Array },
    ib_groups: { Array },
    fgos_groups: { Array },
    deletionMode: { type: Boolean, default: false }
  },
  data() {
    return {
      types: [
        { value: 'base', name: 'Обязательная часть'},
        { value: 'extra', name: 'Внеурочная деятельность'},
      ],
      levels: [
        { value: 'noo', name: 'Начальная школа'},
        { value: 'ooo', name: 'Средняя школа'},
        { value: 'soo', name: 'Старшая школа'},
      ]
    }
  },
  methods: {
    
  },
  mounted() {
  }
}
</script>
  
<style scoped>
.form-edit {
  max-width: 100%;
  margin-top: 10px;
}
.form-title {
  font-size: 1.2em;
  font-weight: 700;
}
</style>