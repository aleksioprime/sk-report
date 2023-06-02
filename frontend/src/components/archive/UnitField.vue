<template>
  <div class="unit-field">
    <div class="unit-field-label">{{ textField[fieldName].label }}</div>
    <div class="unit-field-data" :class="{ 'unit-field-editing': fieldEdit && checkLoad }">
      <transition name="slide-fade">
        <div v-if="!(fieldEdit && checkLoad)" class="d-flex">
          <div v-if="checkData" class="w-100 me-2">
            <slot name="read" :field="fieldName"></slot>
          </div>
          <div v-else>{{ txtNoData }}</div>
          <button class="unit-field-edit" @click="editField"></button>
        </div>
        <div v-else>
          <div class="unit-field-description">{{ textField[fieldName].description }}</div>
          <div class="unit-field-warning">{{ textField[fieldName].warning }}</div>
          <slot name="edit" :field="fieldName"></slot>
          <button class="unit-field-done" @click="saveField">Сохранить</button>
          <button class="unit-field-cancel" @click="cancelField">Отмена</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { toRefs } from 'vue';

export default {
  name: 'unit-field',
  props: {
    txtNoData: { type: String, default: 'Нет данных' },
    checkLoad: { type: Boolean, default: true },
    fieldEditing: { type: String, default: '' },
    fieldName: { type: String, default: '' },
    fieldData: [String, Number, Array, Boolean, Object],
  },
  setup(props) {
    const { fieldEditing } = toRefs(props)
    return {
      fieldEditing
    }
  },
  data() {
    return {
      fieldEdit: false,
      textField: {
        title: {
          label: 'Название юнита',
          description: 'Напишите название юнита'
        },
        subjects: {
          label: 'Предметы',
          description: 'Добавьте учебные предметы и уровни их изучения в список. При добавлении нескольких предметов юнит становится междисциплинарным',
          warning: 'Внимание: при изменении учебных предметов информация о выбранных критериях оценивания, предметных концепциях и целях может быть удалена',
        },
        authors: {
          label: 'Учителя',
          description: 'Выберите авторов юнита'
        },
        class_year: {
          label: 'Год обучения',
          description: 'Выберите год преподавания юнита в MYP',
        },
        hours: {
          label: 'Часы',
          description: 'Укажите количество часов'
        },
        description: {
          label: 'Описание',
          description: 'Укажите краткое описание юнита, включая его значение и результат изучения'
        },
        key_concepts: {
          label: 'Ключевые концепции',
          description: 'Определите одну ключевую концепцию, которая будет направлять развитие юнита'
        },
        related_concepts: {
          label: 'Предметные концепции',
          description: 'Выберите предметные концепции'
        },
        conceptual_understanding: {
          label: 'Концептуальное понимание',
          description: 'Напишите повествовательное предложение, которое отражает взаимосвязь между ключевой и предметными концепциями'
        },
        global_context: {
          label: 'Глобальный контекст',
          description: 'Выберите один из шести глобальных контекстов MYP для преподавания и обучения',
          warning: 'Внимание: при изменении глобального контекста информация о выбранных линиях исследований может быть удалена'
        },
        explorations: {
          label: 'Линии исследования',
          description: 'Укажите возможные линии исследования в юните'
        },
        statement_inquiry: {
          label: 'Формулировка исследования',
          description: 'Сформулируйте утверждение, описывающее концептуальное понимание, которое вы хотите, чтобы студенты запомнили в ходе изучения данного юнита'
        },
        aims: {
          label: 'Общие цели',
          description: 'Выберите, какие общие цели будут достигнуты в данном юните'
        },
        criteria: {
          label: 'Критерии оценивания',
          description: 'Выберите, какие критерии оценивания МУР будут использоваться в данном юните',
          warning: 'Внимание: при изменении критериев оценивания будут удалены связанные предметные цели и записи в карте ATL-навыков'
        },
        strands: {
          label: 'Цели предметной группы',
          description: 'Выберите какие предметные цели будут достигнуты в юните',
          warning: 'Внимание: при изменении целей будут удалены связанные записи в карте ATL-навыков'
        },
        content: {
          label: 'Содержание',
          description: 'Опишите содержание юнита (темы, знания и умения)'
        },
        skills: {
          label: 'Умения',
          description: 'Опишите, какие умения позволят студенту достичь поставленных целей и выполнить задания итоговой работы'
        },
        learner_profile: {
          label: 'Выбор профилей студента IB',
          description: 'Выберите характеристики профиля студента, которые будут развиваться в ходе изучения юнита'
        },
        description_lp: {
          label: 'Описание развития выбранных профилей',
          description: 'Опишите, как вы будете информировать студентов о развитии качеств профиля студента'
        },
        international_mindedness: {
          label: 'Межкультурное понимание',
          description: 'Опишите, как данный юнит позволит студентам обсудить вопросы глобального значения и / или анализировать проблему с разных культурных точек зрения'
        },
        academic_integrity: {
          label: 'Академическая честность',
          description: 'Опишите, как принципы академической честности будут реализовываться в ходе изучения данного юнита'
        },
        language_development: { 
          label: 'Языковое развитие',
          description: 'Опишите, как в ходе изучения данного юнита будет будет поддерживаться языковое развитие студентов'
        },
        infocom_technology: {
          label: 'Использование средств ИКТ',
          description: 'Опишите пути развития информационной грамотности и использования ИКТ в данном юните'
        },
        service_as_action: { 
          label: 'Служение как действие', 
          description: 'В какой степени данный юнит вовлекает студентов в действия по служению обществу? Что я могу сделать, чтобы использовать данный юнит для развития служения обществу? Какие из следующих результатов обучения поддерживают данный юнит?'
        },
        formative_assessment: { 
          label: 'Текущее оценивание', 
          description: 'Предоставьте краткое описание заданий текущего оценивания'
        },
        summative_assessment_task: {
          label: 'Итоговое оценивание (задания)',
          description: 'Предоставьте краткое описание итогового(ых) задания(ий)' 
        },
        summative_assessment_soi: {
          label: 'Итоговое оценивание (взаимосвязь с исследовательским утверждением)',
          description: 'Опишите взаимосвязь итогового задания с исследовательским утверждением'
        },
        peer_self_assessment: {
          label: 'Взаимное и самооценивание',
          description: 'Напишите возможности, которые будут у студентов для участия во взаимной и самооценке'
        },
        standardization_moderation: {
          label: 'Стандартизация и модерация',
          description: 'Опишите процесс стандартизации оценки и процедуры модерации'
        },
        prior_experiences: { 
          label: 'Предыдущий опыт обучения',
          description: 'Опишите предыдущий опыт обучения студентов, связанный с данным юнитом'
        },
        learning_experiences: {
          label: 'Учебная деятельность',
          description: 'Изложите в общих чертах процесс обучения, четко описав, что делают студенты, и напишите этапы, на которых происходит преподавание и усвоение знаний'
        },
        teaching_strategies: { 
          label: 'Стратегии преподавания',
          description: 'Изложите в общих чертах процесс обучения, четко описав, что делают студенты, и напишите этапы, на которых происходит преподавание и усвоение знаний'
        },
        student_expectations: { 
          label: 'Ожидания студентов',
          description: 'Опишите, как студенты узнают, что от них ожидается'
        },
        feedback: { 
          label: 'Обратная связь',
          description: 'Опишите, как обратная связь будет использоваться для поддержки и улучшения обучения студентов во время изучения данного юнита',
        },
        differentiation: { 
          label: 'Дифференциация',
          description: 'Опишите конкретные стратегии, которые будут учитывать разнообразие обучения с точки зрения содержания, процесса и продукта'
        },
        form_integration: { 
          label: 'Формы интеграции',
          description: 'Опишите формы интеграции'
        },
        purpose_integration: { 
          label: 'Цель интеграции',
          description: 'Опишите цель интеграции'
        },
        interdisciplinary_links: { 
          label: 'Междисциплинарные связи',
          description: 'Опишите междисциплинарные связи'
        },
        resources: { 
          label: 'Ресурсы',
          description: 'Укажите ресурсы'
        },
        inter_aims: { 
          label: 'Общие цели',
          description: 'Выберите междисциплинарные общие цели'
        },
        inter_criteria: { 
          label: 'Критерии оценивания',
          description: 'Выберите междисциплинарные критерии оценивания',
          warning: 'Внимание: при изменении междисциплинарных критериев оценивания могут быть удалены специальные цели',
        },
        inter_strands: { 
          label: 'Специальные цели',
          description: 'Выберите междисциплинарные специальные цели'
        },
      },
    }
  },
  methods: {
    saveField() {
      this.fieldEdit = false;
      this.$emit('save', true)
    },
    cancelField() {
      this.fieldEdit = false;
      this.$emit('cancel', this.fieldName);
    },
    editField() {
      this.fieldEdit = true;
      this.$emit('edit', this.fieldName);
    },
  },
  computed: {
    checkData() {
      if (Array.isArray(this.fieldData)) {
        return Boolean(this.fieldData.length)
      } else  {
        return Boolean(this.fieldData)
      }
    },
  },
  watch: {
    fieldEditing() {
      if (this.fieldEditing != this.fieldName) {
        if (this.fieldEdit) { this.cancelField() }
      }
    }
  }
}
</script>