<template>
  <div class="unit-field-data"> 
    <table class="table table-bordered">
      <thead>
        <tr>
          <th scope="col" style="width: 20%">ATL</th>
          <th scope="col">Предметная цель</th>
          <th scope="col" style="width: 40%">Описание учебных действий</th>
          <th style="width: 40px"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="map in unit.atlmapping" :key="map.id" :class="{'item-editing': selectItem == map.id}">
          <td>
            {{ map.atl.name_eng }} <span v-if="map.atl.description_eng"><i>({{ map.atl.description_eng }})</i></span><br>
            <b>{{ map.atl.cluster.name_eng }}</b>
          </td>
          <td><b>{{ map.objective.strand.criterion.letter }}{{ map.objective.strand.letter }}:</b> {{ map.objective.name_eng }}</td>
          <td>{{ map.action }}</td>
          <td>
            <div class="img-btn-all">
              <div class="img-btn-edit" @click="editButton(map)"></div>
              <div class="img-btn-del" @click="showModalDelete(map)"></div>
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="4">
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
                    <select id="objective" class="form-select mb-2" v-model="mapping.objective_id">
                      <option value="-">Выберите предметную цель</option>
                      <option v-for="(ob, i) in unit.objectives" :key="i" :value="ob.id">
                        {{ ob.strand.criterion.letter }}{{ ob.strand.letter }}: {{ ob.name_eng.slice(0, 30) }}...
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
import { mapState } from 'vuex'
import { getATLSkills } from "@/hooks/unit/getUnitMYPEdit";


export default {
  name: 'unit-atl-mapping',
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
      const url = `${this.api}/unitplans/myp/atlmapping`;
	    const config = this.configJWT;
      this.axios.post(url, this.mapping, config)
        .then(() => {
          this.mapping = {};
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Функция кнопки "Сохранить" при редактировании записи
    submitEdit(){
      this.editMode = false;
      const url = `${this.api}/unitplans/myp/atlmapping/${this.mapping.id}`;
	    const config = this.configJWT;
      this.axios.put(url, this.mapping, config)
        .then(() => {
          this.mapping = {};
          this.selectItem = 0;
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
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
      this.mapping.objective_id = item.objective.id;
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
      const url = `${this.api}/unitplans/myp/atlmapping/${this.selectItem}`;
	    const config = this.configJWT;
      this.axios.delete(url, config)
        .then(() => {
          this.$emit('update');
          this.modalDelete.hide();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.modalDelete = new Modal(`#modalDelete${this.idName}`, { backdrop: 'static' });
  },
  computed: {
    ...mapState({
      api: state => state.base.baseAPI,
      configJWT: state => state.base.configJWT,
    }),
  },
  watch: {
    addMode() {
      if (this) {
        this.mapping.atl_id = '-';
        this.mapping.objective_id = '-';
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