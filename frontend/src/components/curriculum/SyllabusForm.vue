<template>
  <div class="form-edit">
    <div class="form-title">
      <div v-if="deletionMode">Удаление нагрузки</div>
      <div v-else-if="editableData.id">Редактирование нагрузки</div>
      <div v-else>Добавление нагрузки</div>
    </div>
    <div v-if="deletionMode">Вы действительно хотите удалить эту нагрузку?</div>
    <div v-else>
      <div class="row">
        <div class="col-md">
          <!-- <select id="subject" class="form-select my-1" v-model="editableData.subject_id" :disabled="disableSubject">
            <option :value="null">Выберите предмет</option>
            <option v-for="sb in subjects" :key="sb.id" :value="sb.id">
              {{ sb.name_rus }}
            </option>
          </select> -->
          <div  v-if="!disableSubject">
            <div>Выберите предмет</div>
            <!-- <div class="radiobutton-wrapper">
              <div v-for="sb in subjects" :key="sb.id" class="radiobutton">
                <input type="radio" :value="sb.id" :id="'sb-' + sb.id" v-model="editableData.subject_id">
                <label :for="'sb-' + sb.id">{{ sb.name_rus }}&nbsp;(<span v-if="sb.group_ib">{{ sb.group_ib.program.toUpperCase() }}</span><span v-else>ФГОС</span>)</label>
              </div>
            </div> -->
            
            <search-one-choice :items="subjects" :searchedField="'name_rus'"
              v-model:editableItem="editableData.subject_id">
              <template v-slot:selected="data">{{ data.item.name_rus }}&nbsp;(<span v-if="data.item.group_ib">{{ data.item.group_ib.program.toUpperCase() }}</span><span v-else>ФГОС</span>)</template>
              <template v-slot:found="data">{{ data.item.name_rus }}&nbsp;(<span v-if="data.item.group_ib">{{ data.item.group_ib.program.toUpperCase() }}</span><span v-else>ФГОС</span>)</template>
            </search-one-choice>
          </div>
          <div v-else></div>
        </div>
        <!-- <div class="col-md-4">
        <select id="class_year" class="form-select my-1" v-model="editableData.class_year_id" :disabled="disableClassYear">
          <option :value="null">Выберите класс</option>
          <option v-for="(cy, i) in years" :key="i" :value="cy.id">
            {{ cy.year_rus }} класс
          </option>
        </select>
      </div> -->
      </div>
      <div class="row mt-2">
        <div class="col-md">
          <div>Выберите классы</div>
          <div class="checkbutton-wrapper">
            <div v-for="cy in years" :key="cy.id" class="checkbutton">
              <input type="checkbox" :value="cy.id" :id="'year-' + cy.id" v-model="editableData.years_ids">
              <label :for="'year-' + cy.id">{{ cy.year_rus }} класс</label>
            </div>
          </div>
        </div>
      </div>
      <div class="my-2 hours">
        <input v-model="editableData.hours" type="text" placeholder="Кол-во часов" class="form-control my-1">
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
  name: 'SyllabusForm',
  props: {
    editableData: {
      type: Object, default: {
        subject_id: null,
        years_ids: [],
      }
    },
    subjects: { Array },
    years: { Array },
    deletionMode: { type: Boolean, default: false }
  },
  setup(props) {
    return {
    }
  },
  data() {
    return {
      disableSubject: false,
      disableClassYear: false,
    }
  },
  methods: {

  },
  mounted() {
    if (this.editableData.subject_id || this.editableData.id) {
      this.disableSubject = true;
    }
    // if (this.editableData.years_ids.length) {
    //   this.disableClassYear = true;
    // }
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

.radiobutton-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.hours {
  max-width: 150px;
}
.radiobutton label {
  display: block;
}
</style>