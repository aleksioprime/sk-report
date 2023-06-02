<template>
  <div class="form-edit">
    <div class="form-title">
      <span v-if="deletionMode">Удаление нагрузки</span>
      <span v-else-if="editableData.id">Редактирование нагрузки</span>
      <span v-else>Добавление нагрузки</span>
    </div>
    <div v-if="deletionMode">Вы действительно хотите удалить эту нагрузку?</div>
    <div v-else>
      <div class="row">
        <div class="col-md">
          <select id="class_year" class="form-select my-1" v-model="editableData.subject_id" :disabled="disableSubject">
            <option :value="null">Выберите предмет</option>
            <option v-for="sb in subjects" :key="sb.id" :value="sb.id">
              {{ sb.name_rus }}
            </option>
          </select>
        </div>
        <div class="col-md-2">
          <input v-model="editableData.hours" type="text" placeholder="Кол-во часов" class="form-control my-1">
        </div>
      </div>
      <div class="row mt-2">
        <div class="col-md">
          <div>Выберите классы</div>
          <div class="checkbutton-wrapper">
            <div v-for="gr in groups" :key="gr.id" class="checkbutton">
              <input type="checkbox" :value="gr.id" :id="'group-' + gr.id" v-model="editableData.groups_ids">
              <label :for="'group-' + gr.id">{{ gr.class_year.year_rus }}{{ gr.letter }} класс</label>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div>Выберите учителя</div>
          <search-one-choice :items="teachers" :searchedField="'last_name'"
            v-model:editableItem="editableData.teacher_id">
            <template v-slot:selected="data">{{ data.item.full_name }}</template>
            <template v-slot:found="data">{{ data.item.short_name }}</template>
          </search-one-choice>
        </div>
      </div>
    </div>
    
    <div class="d-flex justify-content-end">
      <button class="btn btn-success" @click="$emit('apply', this.editableData)">ОК</button>
      <button class="btn btn-cancel" @click="$emit('cancel')">Отмена</button>
    </div>
  </div>
</template>
  
<script>

export default {
  name: 'WorkLoadForm',
  props: {
    editableData: { type: Object, default: {
      subject_id: null,
      groups_ids: [],
      teacher_id: null,
    } },
    subjects: { Array },
    groups: { Array },
    teachers: { Array },
    deletionMode: { type: Boolean, default: false }
  },
  setup(props) {
    return {
    }
  },
  data() {
    return {
      disableSubject: false,
      disableGroup: false,
    }
  },
  methods: {
    
  },
  mounted() {
    if (this.editableData.subject_id || this.editableData.id) {
      this.disableSubject = true;
    }
    if (this.editableData.class_year_id) {
      this.disableGroup = true;
    }
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
.checkbutton-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin: 10px 0;
}
</style>