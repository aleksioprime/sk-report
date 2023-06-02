<template>
  <div class="unit-field-data">
    <div class="mb-2">
      <span>{{ categoryText.title }}</span><br>
      <small>{{ categoryText.description }}</small>
    </div>
    <div v-if="filteredReflections.length" class="my-2">
      <div v-for="rf in filteredReflections" :key="rf.id" class="my-2">
        <div class="d-flex border p-2">
          <div>
            <div>{{ rf.post }}</div>
            <div>- {{ rf.author.user.last_name }} {{ rf.author.user.first_name }} {{ rf.author.user.middle_name }}</div>
          </div>
          <div v-if="authUser.teacher.id == rf.author.id" class="img-btn-all ms-auto">
            <div class="img-btn-edit" @click="editButton(rf)"></div>
            <div class="img-btn-del" @click="showModalDelete(rf)"></div>
          </div>
        </div>
      </div>
    </div>
    <transition name="slide-fade">
      <div ref="form">
        <div class="btn btn-primary" @click="addButton" v-if="!addMode && !editMode">Новый пост</div>
        <div><b><span v-if="addMode">Добавление нового поста рефлексии</span><span v-if="editMode">Редактирование поста</span></b></div>
        <div v-if="addMode || editMode">
          <div class="my-2">
            <textarea class="form-control mb-2" type="text" v-model="reflection.post" placeholder="Вводите здесь текст..."></textarea>
            <div class="my-2">
              <select id="author" class="form-select mb-2" v-model="reflection.author_id">
                <option value="-">Выберите автора</option>
                <option v-for="(author, i) in teachers" :key="i" :value="author.id">
                  {{ author.user.last_name }} {{ author.user.first_name }} {{ author.user.middle_name }}
                </option>
              </select>
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
    <modal-delete :idName="idName + categoryValue" :del="true" @cancel="hideModalDelete" @delete="submitDelete">
      <div>Вы действительно хотите удалить эту запись?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';
import { getTeachers } from "@/hooks/unit/getUnitMYPList"

export default {
  name: 'unit-myp-view-reflection',
  props: {
    unit: Object,
    categoryValue: '',
    categoryText: Object,
  },
  setup(props) {
    // Получение функции запроса списка учителей
    const { teachers, getTeachersData } = getTeachers();
    return {
      teachers, getTeachersData
    }
  },
  data() {
    return {
      idName: 'Reflection',
      modalDelete: {},
      editMode: false,
      addMode: false,
      reflection: {},
      selectItem: 0,
    }
  },
  methods: {
    // Функция активации режима добавления записи
    addButton() {
      this.getTeachersData();
      this.reflection.author_id = this.authUser.teacher.id;
      this.addMode = true;
      this.editMode = false;
      this.$refs.form.scrollIntoView(true);
    },
    // Функция активации режима редактирования записи
    editButton(item) {
      this.getTeachersData();
      this.editMode = true;
      this.addMode = false;
      this.selectItem = item.id;
      this.reflection = Object.assign({}, item);
    },
    // Функция кнопки "Отмена"
    cancelButton() {
      this.editMode = false;
      this.addMode = false;
      this.reflection = {};
      this.selectItem = 0;
    },
    // Вызов и скрытие модального окна
    showModalDelete(item) {
      this.selectItem = item.id;
      this.modalDelete.show();
    },
    hideModalDelete() {
      this.selectItem = 0;
      this.modalDelete.hide();
    },
    // Функция кнопки "Добавить" при добавлении записи
    submitAdd() {
      this.addMode = false;
      this.reflection.planner = this.unit.id;
      this.reflection.type_post = this.categoryValue;
      this.axios.post('/unitplans/myp/reflection', this.reflection)
        .then(() => {
          this.reflection = {};
          this.$emit('update');
        });
    },
    // Функция кнопки "Сохранить" при редактировании записи
    submitEdit(){
      this.editMode = false;
      this.axios.put(`/unitplans/myp/reflection/${this.reflection.id}`, this.reflection)
        .then(() => {
          this.reflection = {};
          this.selectItem = 0;
          this.$emit('update');
        });
    },
    // Функция удаления вопроса
    submitDelete() {
      this.axios.delete(`/unitplans/myp/reflection/${this.selectItem}`)
        .then(() => {
          this.$emit('update');
          this.modalDelete.hide();
        });
    },
  },
  mounted() {
    this.modalDelete = new Modal(`#modalDelete${this.idName}${this.categoryValue}`, { backdrop: 'static' });
  },
  computed: {
    ...mapGetters(['authUser']),
    filteredReflections () {
      return this.unit.reflections.filter((rf) => rf.type_post == this.categoryValue)
    }
  },
}
</script>

<style scoped>
.img-btn-all {
  display: flex;
}

.img-btn-edit,
.img-btn-del {
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