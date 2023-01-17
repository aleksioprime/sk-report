<template>
  <div>
    <div v-for="op in options" :key="op.id">
      <div class="form-check ms-3">
        <input class="form-check-input" type="radio" :name="nameField" :value="op.id" :id="nameField + '-' + op.id" v-model="modelValue" @change="changeOption">
        <label class="form-check-label" :for="nameField + '-' + op.id">
          <slot :field="op">
          
          </slot>
        </label>
      </div>
    </div>
  </div>
</template>
  
<script>
  export default {
    name: 'field-radio-edit',
    props: {
      modelValue: [ String, Number, Boolean, Array ],
      nameField: { type: String }, 
      options: { type: Array, default: () => [] },
    },
    methods: {
      changeOption(event) {
        this.$emit('update:modelValue', this.modelValue);
      }
    },
  }
</script>