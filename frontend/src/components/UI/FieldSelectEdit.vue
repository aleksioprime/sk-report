<template>
  <div>
    <select id="subject" class="form-select" v-model="modelValue" @change="changeOption">
      <option v-for="(op, i) in options" :key="i" :value="op.id">
        {{ op.name_rus }}
      </option>
    </select>
  </div>
</template>
  
<script>
  export default {
    name: 'field-select-edit',
    props: {
      modelValue: [String, Number], 
      options: {
        type: Array,
        default: () => []
      },
    },
    data() {
      return {
      }
    },
    methods: {
      changeOption(event) {
        this.$emit('update:modelValue', event.target.value)
      }
    },
  }
</script>