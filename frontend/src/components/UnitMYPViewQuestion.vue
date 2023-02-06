<template>
  <div class="unit-field-data"> 
    <table class="table">
      <thead>
        <tr>
          <th scope="col" style="width: 150px">Тип</th>
          <th scope="col">Вопрос</th>
          <th style="width: 40px"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="inq in unit.inquestions" :key="inq.id" :class="{'item-editing': selectItem == inq.id}">
          <td><div class="badge" :class="classTypeQuestion(inq)">{{ findType(inq.type_inq).name }}</div></td>
          <td>
            <div>{{ inq.question }}</div>
            <div v-if="inq.line">{{ inq.line }}</div>
          </td>
          <td>
            <div class="img-btn-all">
              <div class="img-btn-edit" @click="editButton(inq)"></div>
              <div class="img-btn-del" @click="showModalDelete(inq)"></div>
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="4">
            <transition name="slide-fade">
            <div ref="form">
              <div class="btn btn-primary" @click="addButton" v-if="!addMode && !editMode">Новый вопрос</div>
              <div><b><span v-if="addMode">Добавление нового вопроса</span><span v-if="editMode">Редактирование вопроса</span></b></div>
              <!-- Поля для добавления или редактирования записи -->
              <div v-if="addMode || editMode">
                <div class="my-2">
                  <textarea class="form-control mb-2" type="text" v-model="inquestion.question" placeholder="Исследовательский вопрос"></textarea>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <select id="subject" class="form-select mb-2" v-model="inquestion.type_inq">
                      <option value="-">Выберите тип</option>
                      <option v-for="(op, i) in options_question" :key="i" :value="op.value">
                        {{ op.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-md">
                    <textarea class="form-control mb-2" type="text" v-model="inquestion.line" placeholder="Линия исследования"></textarea>
                  </div>
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
      <div>Вы действитель хотите удалить этот исследовательский вопрос?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  name: 'unit-myp-view-question',
  props: {
    unit: { type: Object },
  },
  setup(props) {

  },
  data() {
    return {
      idName: 'Question',
      modalDelete: {},
      editMode: false,
      addMode: false,
      inquestion: {},
      selectItem: 0,
      options_question: [
        { name: "Фактический", value: 'Factual' },
        { name: "Концептуальный", value: 'Conceptual' },
        { name: "Дискуссионный", value: 'Debatable' },
      ]
    }
  },
  methods: {
    // Получение типа вопроса по значению
    findType(value) {
      return this.options_question.find(item => item.value == value); 
    },
    // Функция кнопки "Отмена"
    cancelButton() {
      this.editMode = false;
      this.addMode = false;
      this.inquestion = {};
      this.selectItem = 0;
    },
    // Функция кнопки "Добавить" при добавлении записи
    submitAdd() {
      this.addMode = false;
      this.inquestion.planner = this.unit.id;
      this.axios.post('/unitplans/myp/inquestion', this.inquestion)
        .then(() => {
          this.inquestion = {};
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Функция кнопки "Сохранить" при редактировании записи
    submitEdit(){
      this.editMode = false;
      this.axios.put(`/unitplans/myp/inquestion/${this.inquestion.id}`, this.inquestion)
        .then(() => {
          this.inquestion = {};
          this.selectItem = 0;
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Функция активации режима добавления записи
    addButton() {
      this.addMode = true;
      this.editMode = false;
      this.$refs.form.scrollIntoView(true);
    },
    // Функция активации режима редактирования записи
    editButton(item) {
      this.editMode = true;
      this.addMode = false;
      this.selectItem = item.id;
      this.inquestion = Object.assign({}, item);
    },
    showModalDelete(item) {
      this.selectItem = item.id;
      this.modalDelete.show();
    },
    hideModalDelete() {
      this.selectItem = 0;
      this.modalDelete.hide();
    },
    // Функция удаления вопроса
    submitDelete() {
      this.axios.delete(`${this.api}/unitplans/myp/inquestion/${this.selectItem}`)
        .then(() => {
          this.$emit('update');
          this.modalDelete.hide();
        });
    },
    classTypeQuestion(inq) {
      return {
        'text-bg-primary': inq.type_inq == 'Factual',
        'text-bg-info': inq.type_inq == 'Conceptual',
        'text-bg-warning': inq.type_inq == 'Debatable',
      }
    }
  },
  mounted() {
    this.modalDelete = new Modal(`#modalDelete${this.idName}`, { backdrop: 'static' });
  },
  computed: {
    
  },
  watch: {
    addMode() {
      if (this) {
        this.inquestion.type_inq = '-';
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