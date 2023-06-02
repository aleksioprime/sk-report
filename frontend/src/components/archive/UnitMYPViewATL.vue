<template>
  <div class="unit-field-data"> 
    <table class="table">
      <thead>
        <tr>
          <th scope="col" style="width: 40%">ATL и предметная цель</th>
          <th scope="col">Описание учебных действий</th>
          <th style="width: 50px"></th>
        </tr>
      </thead>
      <tbody>
        <template v-for="map in unit.atlmapping" :key="map.id" :class="{'item-editing': selectItem == map.id}">
          <tr>
            <td>
              {{ map.atl.name_eng }} <span v-if="map.atl.description_eng"><i>({{ map.atl.description_eng }})</i></span> (<b>{{ map.atl.cluster.name_eng }}</b>)
            </td>
            <td rowspan="2" class="border">
              {{ map.action }}
            </td>
            <td rowspan="2">
              <div class="img-btn-all flex-column">
                <div class="img-btn-edit" @click="editButton(map)"></div>
                <div class="img-btn-del" @click="showModalDelete(map)"></div>
              </div>
            </td>
          </tr>
          <tr>
            <td><b>{{ map.strand.criterion.letter }}{{ map.strand.letter }}:</b> {{ firstLetterBig(map.strand.name_eng) }}</td>
          </tr>
        </template>
        <tr>
          <td colspan="3">
            <transition name="slide-fade">
              <div ref="form">
                <div class="btn btn-primary" @click="addButton" v-if="!addMode && !editMode">Добавить</div>
                <div v-if="addMode || editMode">
                  <div><b><span v-if="addMode">Добавление новой записи</span><span v-if="editMode">Редактирование записи</span></b></div>
                  <!-- Поля для добавления или редактирования записи -->
                  <div class="my-2">
                    <select id="atl" class="form-select mb-2" v-model="mapping.atl_id">
                      <option value="-">Выберите навыки ATL</option>
                      <option v-for="(atl, i) in atlSkills" :key="i" :value="atl.id">
                        {{ atl.name_eng }} ({{ atl.cluster.name_eng }})
                      </option>
                    </select>
                  </div>
                  <div class="my-2">
                    <select id="strand" class="form-select mb-2" v-model="mapping.strand_id">
                      <option value="-">Выберите предметную цель</option>
                      <option v-for="(ob, i) in unit.strands" :key="i" :value="ob.id">
                        <span v-if="unit.subjects.length > 0"><b>{{ ob.criterion.subject_group.name_eng }} - </b></span>{{ ob.criterion.letter }}{{ ob.letter }}: {{ firstLetterBig(ob.name_eng) }}
                      </option>
                    </select>
                  </div>
                  <div class="my-2">
                    <textarea class="form-control mb-2" type="text" v-model="mapping.action" placeholder="Опишите учебные действия"></textarea>
                  </div>
                  <div class="my-2">
                    <button class="btn btn-success me-2" type="button" @click="submitAdd" v-if="addMode" >Добавить</button>
                    <button class="btn btn-success me-2" type="button" @click="submitEdit" v-if="editMode">Сохранить</button>
                    <button class="btn btn-secondary" type="button" @click="cancelButton">Отмена</button>
                  </div>
                </div>
              </div>
            </transition>
          </td>
        </tr>
      </tbody>
    </table>
    <modal-delete :idName="idName" :del="true" @cancel="hideModalDelete" @delete="submitDelete">
      <div>Вы действитель хотите удалить эту запись?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { getATLSkills } from "@/hooks/unit/getUnitMYPEdit";


export default {
  name: 'unit-myp-view-atl',
  props: {
    unit: { type: Object },
  },
  setup(props) {
    // Получение функции запроса всех навыков ATL
    const { atlSkills, getATLSkillsData } = getATLSkills();
    return {
      atlSkills, getATLSkillsData
    }
  },
  data() {
    return {
      idName: 'Mapping',
      modalDelete: {},
      editMode: false,
      addMode: false,
      mapping: {},
      selectItem: 0,
    }
  },
  methods: {
    // Функция кнопки "Отмена"
    cancelButton() {
      this.editMode = false;
      this.addMode = false;
      this.mapping = {};
      this.selectItem = 0;
    },
    // Функция кнопки "Добавить" при добавлении записи
    submitAdd() {
      console.log(this.mapping)
      this.addMode = false;
      this.mapping.planner = this.unit.id;
      this.axios.post('/unitplans/myp/atlmapping', this.mapping)
        .then(() => {
          this.mapping = {};
          this.$emit('update');
        });
    },
    // Функция кнопки "Сохранить" при редактировании записи
    submitEdit(){
      this.editMode = false;
      this.axios.put(`/unitplans/myp/atlmapping/${this.mapping.id}`, this.mapping)
        .then(() => {
          this.mapping = {};
          this.selectItem = 0;
          this.$emit('update');
        });
    },
    // Функция активации режима добавления записи
    addButton() {
      this.getATLSkillsData();
      this.addMode = true;
      this.editMode = false;
      this.$refs.form.scrollIntoView(true);
    },
    // Функция активации режима редактирования записи
    editButton(item) {
      this.getATLSkillsData();
      this.editMode = true;
      this.addMode = false;
      this.selectItem = item.id;
      this.mapping = Object.assign({}, item);
      this.mapping.strand_id = item.strand.id;
      this.mapping.atl_id = item.atl.id;
    },
    showModalDelete(item) {
      this.selectItem = item.id;
      this.modalDelete.show();
    },
    hideModalDelete() {
      this.selectItem = 0;
      this.modalDelete.hide();
    },
    // Функция удаления записи
    submitDelete() {
      this.axios.delete(`/unitplans/myp/atlmapping/${this.selectItem}`)
        .then(() => {
          this.$emit('update');
          this.modalDelete.hide();
        });
    },
    // Функция делает первую букву заглавной в тексте
    firstLetterBig(text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
    },
  },
  mounted() {
    this.modalDelete = new Modal(`#modalDelete${this.idName}`, { backdrop: 'static' });
  },
  watch: {
    addMode() {
      if (this) {
        this.mapping.atl_id = '-';
        this.mapping.strand_id = '-';
      }
    }
  }
}
</script>

<style scoped>
.img-btn-all {
  display: flex;
}
.img-btn-edit, .img-btn-del {
  width: 25px;
  height: 25px;
  cursor: pointer;
  margin-left: 5px;
}
.img-btn-edit {
  background: url('@/assets/img/edit-btn.png') no-repeat 50%;
  background-size: 100%;
}

.img-btn-del {
  background: url('@/assets/img/delete-btn.png') no-repeat 50%;
  background-size: 100%;
}
.item-editing {
  color: red;
}
.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>