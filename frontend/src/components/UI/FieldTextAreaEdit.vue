<template>
  <div>
    <textarea class="form-control unit-field-input" rows="3" v-model="modelValue" @input="updateInput"></textarea>
  </div>
</template>
  
<script>
  export default {
    name: 'field-textarea-edit',
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
        this.$emit('update:modelValue', event.target.value)
      }
    },
  }
</script>