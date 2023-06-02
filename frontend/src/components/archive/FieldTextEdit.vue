<template>
  <div>
    <input class="form-control unit-field-input" type="text" v-model="modelValue" @input="updateInput">
  </div>
</template>
  
<script>
  export default {
    name: 'field-text-edit',
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