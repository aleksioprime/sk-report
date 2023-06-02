<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">{{ fieldText.label }}</div>
      <button v-if="!editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div v-if="checkData">
            <div v-html="fieldData"></div> 
          </div>
          <div v-else>Нет данных</div>
        </div>
        <div v-else>
          <div class="field-description">{{ fieldText.description }}</div>
          <div class="field-warning">{{ fieldText.warning }}</div>
          <div v-show="tinyLoading">
            <editor api-key="j30bef5hr2ipfdbu7b9lww7t4oez2v6f27c94otp9to2j9mk"
              :init="{
                plugins: 'lists link wordcount autoresize',
                menubar: false,
                toolbar: 'undo redo | bold italic | forecolor | alignleft aligncenter alignright alignjustify | bullist numlist ',
                setup: (ed) => {
                  ed.on('init', () => { tinyLoading = true});
                }
              }"
              model-events="change keydown blur focus paste" output-format="html" v-model="editData[fieldName]"/>
          </div>
          <div v-if="!tinyLoading" class="loader">
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
          <div class="field-buttons">
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
import Editor from '@tinymce/tinymce-vue';
export default {
  name: 'unit-field-text',
  components: {
    'editor': Editor
  },
  props: {
    fieldName: { String },
    fieldText: { Object },
    fieldData: { Object },
  },
  setup(props) {
    return {

    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
      tinyLoading: false,
    }
  },
  methods: {
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData)
    },
    cancelField() {
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      this.editData[this.fieldName] = this.fieldData;
    },
  },
  computed: {
    checkData() {
      if (Array.isArray(this.fieldData)) {
        return Boolean(this.fieldData.length)
      } else {
        return Boolean(this.fieldData)
      }
    },
  },
  mounted() {
  },
  watch: {

  }
}
</script>