<template>
  <div>
    <!-- <textarea class="form-control unit-field-input" rows="3" v-model="modelValue" @input="updateInput"></textarea> -->
    <editor api-key="j30bef5hr2ipfdbu7b9lww7t4oez2v6f27c94otp9to2j9mk" 
      :init="{ plugins: 'lists link wordcount autoresize',
               menubar: false,
               toolbar: 'undo redo | bold italic | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist '}" 
      model-events="change keydown blur focus paste" 
      output-format="html"
      v-model="modelValue" @selectionChange="updateInput"/>
  </div>
</template>
  
<script>
  import Editor from '@tinymce/tinymce-vue';


  export default {
    name: 'field-textarea-edit',
    components: {
      'editor': Editor
    },
    props: {
      modelValue: [String, Number], 
    },
    data() {
      return {
        fieldEdit: false,
      }
    },
    methods: {
      updateInput(event) {
        // console.log(event.target)
        this.$emit('update:modelValue', this.modelValue)
      }
    },
  }
</script>