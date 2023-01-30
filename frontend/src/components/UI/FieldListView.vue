<template>
  <div>
    <div v-for="op in options" :key="op.id">
      <slot :field="op">
        
      </slot>
    </div>
  </div>
</template>
  
<script>
  export default {
    name: 'field-list-view',
    props: {
      modelValue: { type: Array, default: () => [] },
      nameField: { type: String }, 
      options: { type: Array, default: () => [] },
    },
  }
</script>