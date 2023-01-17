<template>
  <div class="unit-field-data">
    <div class="mb-2">
      <span>{{ categoryText.title }}</span><br>
      <small>{{ categoryText.description }}</small>
    </div>
    <div v-if="filteredReflections.length" class="my-2">
      <div v-for="rf in filteredReflections" :key="rf.id" class="my-2">
        <div class="d-flex border p-2">
          <div>"{{ rf.post }}" - <span>{{ rf.author.short_name }}</span></div>
          <div v-if="$store.state.auth.authUser.teacher.id == rf.author.id" class="img-btn-all ms-auto">
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
        <!-- Поля для добавления или редактирования записи -->
        <div v-if="addMode || editMode">
          <div class="my-2">
            <textarea class="form-control mb-2" type="text" v-model="reflection.post" placeholder="Вводите здесь текст..."></textarea>
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
      <div>Вы действитель хотите удалить эту запись?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapState } from 'vuex'

export default {
  name: 'unit-reflection',
  props: {
    unit: Object,
    categoryValue: '',
    categoryText: Object,
  },
  setup(props) {

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
      this.addMode = true;
      this.editMode = false;
      this.$refs.form.scrollIntoView(true);
    },
    // Функция активации режима редактирования записи
    editButton(item) {
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
      this.reflection.author_id = this.$store.state.auth.authUser.teacher.id;
      this.reflection.type_post = this.categoryValue;
      console.log(this.reflection)
      const url = `${this.api}/unitplans/myp/reflection`;
	    const config = this.configJWT;
      this.axios.post(url, this.reflection, config)
        .then(() => {
          this.reflection = {};
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Функция кнопки "Сохранить" при редактировании записи
    submitEdit(){
      this.editMode = false;
      const url = `${this.api}/unitplans/myp/reflection/${this.reflection.id}`;
	    const config = this.configJWT;
      this.axios.put(url, this.reflection, config)
        .then(() => {
          this.reflection = {};
          this.selectItem = 0;
          this.$emit('update');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Функция удаления вопроса
    submitDelete() {
      const url = `${this.api}/unitplans/myp/reflection/${this.selectItem}`;
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
    this.modalDelete = new Modal(`#modalDelete${this.idName}${this.categoryValue}`, { backdrop: 'static' });
  },
  computed: {
    ...mapState({
      api: state => state.base.baseAPI,
      configJWT: state => state.base.configJWT,
    }),
    filteredReflections () {
      return this.unit.reflections.filter((rf) => rf.type_post == this.categoryValue)
    }
  },
  watch: {
  }
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