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
            <div v-for="(itemGrouped, group) in groupedArrayData(fieldData, [fieldGroup, 'id'])" :key="group">
              <div class="field-group"><slot name="showGroup" :data="group"></slot></div>
              <div v-for="item in itemGrouped" :key="item.id" class="field-item">
                <slot name="show" :data="item"></slot>
              </div>
            </div>
          </div>
          <div v-else>Нет данных</div>
        </div>
        <div v-else>
          <div class="field-description">{{ fieldText.description }}</div>
          <div class="field-warning">{{ fieldText.warning }}</div>
          <div v-for="(optionsGrouped, group) in groupedArrayData(options, [fieldGroup, 'id'])" :key="group">
            <div class="field-group"><slot name="editGroup" :data="group"></slot></div>
            <div v-for="op in optionsGrouped" :key="op.id">
              <div class="form-check ms-3">
                <input class="form-check-input" type="checkbox" :value="op.id" :id="fieldName + '-' + op.id"
                  v-model="editData[`${fieldName}_ids`]">
                <label class="form-check-label" :for="fieldName + '-' + op.id">
                    <slot name="edit" :data="op"></slot>
                </label>
              </div>
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
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'unit-field-checkbox-grouped',
  props: {
    fieldGroup: { String },
    fieldName: { String },
    fieldText: { Object },
    fieldData: { type: Object },
    options: { type: Array, default: () => [] },
  },
  setup(props) {
    const { groupedArrayData } = getGroupedArray();
    return {
      groupedArrayData
    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
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
      this.editData[`${this.fieldName}_ids`] = this.fieldData.map(item => item.id);
      this.$emit('edit', this.fieldName);
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