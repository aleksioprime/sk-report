<template>
  <div class="mark">
    <div class="mark-item">
      <input :id="`mark-${name}-null`" type="radio" :name="`mark-${name}`" :value="null" v-model="modelValue" @change="changeOption">
      <label :for="`mark-${name}-null`">-</label>
    </div>
    <div class="mark-item" v-for="mark, index in getRange(max_mark)" :key="index">
      <input :id="`mark-${name}-${mark}`" type="radio" :name="`mark-${name}`" :value="mark" v-model="modelValue" @change="changeOption">
      <label :for="`mark-${name}-${mark}`">{{ mark }}</label>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'mark-choice',
  props: {
    max_mark: { Number },
    modelValue: { Number },
    name: { String },
  },
  methods: {
    getRange(value) {
      if (!value || value < 0) {
        return []
      }
      return [...Array(value + 1).keys()]
    },
    changeOption(event) {
      this.$emit('update:modelValue', this.modelValue);
    }
  },
}
</script>

<style>
/* Переключатель */
.mark {
	display: flex;
  background: none;
}
.mark-item {
	float: left;
	display: inline-block;
}
.mark-item input[type=radio] {
	display: none;
}
.mark-item label {
	display: inline-block;
	padding: 0px 15px;   
	line-height: 34px;    
	border: 1px solid var(--bs-secondary);
	cursor: pointer;
	user-select: none;   
}

.mark-item:not(:last-of-type) label {
	border-right: none;  
}

.mark-item:last-of-type label {
  border-radius: 0 10px 10px 0; 
}

.mark-item:first-of-type label {
  border-radius: 10px 0 0 10px; 
}

.mark input[type=radio] + label {
	background: #fff;
  color: #8f8e8e;
}
.mark input[type=radio]:checked + label {
	background: var(--bs-secondary);
  color: #fff;
}

@media screen and (max-width: 992px) {
  .mark-item label  {
    padding: 0 8px;
  }
}

@media screen and (max-width: 768px) {
  .mark-item label  {
    padding: 0 10px;
  }
}
</style>