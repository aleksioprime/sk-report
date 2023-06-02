<template>
  <div v-if="fieldName == 'strands' || fieldName == 'inter_strands'">
    <div v-for="(options, field) in groupedFieldTwo(options, 'criterion', 'subject_group')" :key="field">
      <div class="my-2"><b>{{ getFieldData(criteriaSubjectGroupUnit, field).name_eng }}</b></div>
      <div v-for="(options, field) in groupedField(options, 'criterion')" :key="field">
        <div class="my-2"><b>{{ getFieldData(criteriaUnit, field).letter }}. {{ getFieldData(criteriaUnit, field).name_eng }}</b></div>
        <div v-for="op in options" :key="op.id">
          <div class="form-check ms-3">
            <input class="form-check-input" type="checkbox" :value="op.id" :id="fieldName + '-' + op.id" v-model="modelValue" @change="changeOption">
            <label class="form-check-label" :for="fieldName + '-' + op.id">
              <div>
                <slot :field="op">
              
                </slot>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div v-if="group">
      <div v-for="(options, field) in groupedField(options, 'subject_group')" :key="field">
        <div class="my-2"><b>{{ subjectGroupUnit.find(item => item.id == field).name_eng }}</b></div>
        <div v-for="op in options" :key="op.id">
          <div class="form-check ms-3">
            <input class="form-check-input" type="checkbox" :value="op.id" :id="fieldName + '-' + op.id" v-model="modelValue" @change="changeOption">
            <label class="form-check-label" :for="fieldName + '-' + op.id">
              <div>
                <slot :field="op">
              
                </slot>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
    <div v-else :class="horizontalStyle">
      <div v-for="op in options" :key="op.id">
        <div class="form-check ms-3">
          <input class="form-check-input" type="checkbox" :value="op.id" :id="fieldName + '-' + op.id" v-model="modelValue" @change="changeOption">
          <label class="form-check-label" :for="fieldName + '-' + op.id">
            <div>
              <slot :field="op">
            
              </slot>
            </div>
          </label>
        </div>
      </div>
    </div>
    
  </div>
</template>
  
<script>
  export default {
    name: 'field-checkbox-edit',
    props: {
      modelValue: { type: Array, default: () => [] },
      fieldName: { type: String }, 
      options: { type: Array, default: () => [] },
      group: { type: Boolean },
    },
    methods: {
      changeOption(event) {
        this.$emit('update:modelValue', this.modelValue);
      },
      groupedField(field, name) {
        let groupedObject = field.reduce((acc, obj) => {
          const property = obj[name].id;
          acc[property] = acc[property] || [];
          acc[property].push(obj);
          return acc;
        }, {});
        return groupedObject;
      },
      groupedFieldTwo(field, first, second) {
        let groupedObject = field.reduce((acc, obj) => {
          const property = obj[first][second].id;
          acc[property] = acc[property] || [];
          acc[property].push(obj);
          return acc;
        }, {});
        return groupedObject;
      },
      getFieldData(value, field) {
        return value.find(item => item.id == field);
      }
    },
    computed: {
      // Переменная для выборки предменых групп из текущих предметов юнита
      subjectGroupUnit() {
        let objArray = this.options.map(sb => sb.subject_group)
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
      },
      criteriaSubjectGroupUnit() {
        let objArray = this.options.map(cr => cr.criterion).map(sb => sb.subject_group).flat();
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
      },
      // Переменная для выборки критериев из текущих стрендов юнита
      criteriaUnit() {
        let objArray = this.options.map(sb => sb.criterion)
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
      },
      // directionSubjectGroupUnit() {
      //   let objArray = this.options.map(cr => cr.subject_directions).flat().map(sb => sb.subject_group).flat();
      //   return [...new Map(objArray.map((item) => [item["id"], item])).values()]
      // }
      horizontalStyle() {
        return {
          'd-flex': this.fieldName=='related_concepts',
          'flex-wrap': this.fieldName=='related_concepts',
        }
      },
    }
  }
</script>