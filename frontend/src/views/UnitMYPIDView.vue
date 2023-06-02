<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/myp">Вернуться к списку юнитов</a></template>
      <template v-slot:header>MYP: Работа с междисциплинарным юнитом</template>
    </base-header>
    <transition name="fade">
      <div class="row" v-if="!isUnitIDLoading">
        <div class="col-sm myp-sidebar">
          <!-- Процент заполнения юнита -->
          <div>Заполнение юнита</div>
          <div class="progress" style="height: 20px;">
            <div class="progress-bar" role="progressbar" :style="`width: ${interdisciplinaryUnit.fullness}%`" :aria-valuenow="interdisciplinaryUnit.fullness" aria-valuemin="0" aria-valuemax="100">{{ interdisciplinaryUnit.fullness }}%</div>
          </div>
          <nav id="navbar-myp" class="navbar-myp">
            <nav class="nav nav-pills flex-column">
              <a class="nav-link myp-group" href="#myp-base">Основная информация</a>
              <a class="nav-link myp-group" href="#myp-inquiry">Исследование</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('key_concepts')" href="#key_concepts">Ключевые концепты</a>
                <a class="nav-link myp-field" :class="checkField('related_concepts')" href="#related_concepts">Предметные концепты</a>
                <a class="nav-link myp-field" :class="checkField('conceptual_understanding')" href="#conceptual_understanding">Концептуальное понимание</a>
                <a class="nav-link myp-field" :class="checkField('global_context')" href="#global_context">Глобальный контекст</a>
                <a class="nav-link myp-field" :class="checkField('explorations')" href="#explorations">Линии исследования</a>
                <a class="nav-link myp-field" :class="checkField('statement_inquiry')" href="#statement_inquiry">Формулировка исследования</a>
                <a class="nav-link myp-field" :class="checkField('inquiry_questions')" href="#inquiry_questions">Исследовательские вопросы</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-objectives">Образовательные цели</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('aims')" href="#aims">Общие цели</a>
                <a class="nav-link myp-field" :class="checkField('criteria')" href="#criteria">Критерии оценивания</a>
                <a class="nav-link myp-field" :class="checkField('strands')" href="#strands">Специальные цели</a>
                <a class="nav-link myp-field" :class="checkField('tasks')" href="#tasks">Задания МДП</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-teaching-assessment">Учебная деятельность и оценивание</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('introduction')" href="#introduction">Введение в МДП</a>
                <a class="nav-link myp-field" :class="checkField('learning_teaching')" href="#learning_teaching">Учебная деятельность</a>
                <a class="nav-link myp-field" :class="checkField('formative_assessment')" href="#formative_assessment">Текущее оценивание</a>
                <a class="nav-link myp-field" :class="checkField('summative_assessment')" href="#summative_assessment">Итоговое оценивание</a>
                <a class="nav-link myp-field" :class="checkField('differentiation')" href="#differentiation">Дифференциация</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-reflections">Рефлексия</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('reflections', type='Prior')"  href="#reflections_prior">До начала изучения</a>
                <a class="nav-link myp-field" :class="checkField('reflections', type='During')" href="#reflections_during">В процессе изучения юнита</a>
                <a class="nav-link myp-field" :class="checkField('reflections', type='After')" href="#reflections_after">По окончании изучения юнита</a>
              </nav>
            </nav>
          </nav>
        </div>
        <div class="col-sm">
          <div data-bs-spy="scroll" data-bs-target="#navbar-myp" data-bs-smooth-scroll="true" tabindex="0">
            <!-- ОСНОВНАЯ ИНФОРМАЦИЯ -->
            <div id="myp-base" class="myp-header">Основная информация</div>
            <!-- Название юнита -->
            <unit-field-string id="title" :fieldName="'title'" :fieldText="fieldText.title" :fieldData="interdisciplinaryUnit.title"
              @save="unitIDFieldSave" />
            <div class="row">
              <div class="col-md-5">
                <!-- Количество часов -->
                <unit-field-string id="hours" :fieldName="'hours'" :fieldText="fieldText.hours" :fieldData="interdisciplinaryUnit.hours"
                  @save="unitIDFieldSave" />
              </div>
              <div class="col-md">
                <!-- Год обучения -->
                <unit-field-select id="class_year" :fieldName="'class_year'" :fieldText="fieldText.class_year"
                  :fieldData="interdisciplinaryUnit.class_year" :options="years" @save="unitIDFieldSave" @edit="unitFieldEdit">
                  <template v-slot:show="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
                  <template v-slot:edit="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
                </unit-field-select>
              </div>
            </div>
            <!-- Цель интеграции -->
            <unit-field-text id="purpose_integration" :fieldName="'purpose_integration'" :fieldText="fieldText.purpose_integration" 
            :fieldData="interdisciplinaryUnit.purpose_integration" @save="unitIDFieldSave" />
            <!-- Предметные юниты -->
            <unit-field-checkbox id="unitplan_myp" :fieldName="'unitplan_myp'" :fieldText="fieldText.unitplan_myp"
              :fieldData="interdisciplinaryUnit.unitplan_myp" :options="unitListMYP" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">
                <div class="unit-wrapper" @click="$router.push(`/myp/${field.data.id}`)">
                  <div><b>{{ field.data.title }}</b> ({{ field.data.subject.name_rus }})</div>
                  <div class="ms-2">Учителя: <span v-for="(author, index) in field.data.authors" :key="author.id">
                    {{ author.first_name }} {{ author.middle_name }} {{ author.last_name }}<span v-if="++index !== field.data.authors.length">,&nbsp;</span>
                  </span></div>
                </div>
              </template>
              <template v-slot:edit="field">
                <div><b>{{ field.data.title }}</b> <span v-if="field.data.subject">({{ field.data.subject.name_rus }})</span></div>
              </template>
            </unit-field-checkbox>
            <!-- ИССЛЕДОВАНИЕ -->
            <div id="myp-inquiry" class="myp-header">Исследование</div>
            <!-- Ключевые концепции -->
            <unit-field-checkbox id="key_concepts" :fieldName="'key_concepts'" :fieldText="fieldText.key_concepts"
              :fieldData="interdisciplinaryUnit.key_concepts" :options="keyConcepts" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field"><b>{{ field.data.name_eng }}</b><br><small>
                {{ field.data.description_eng }}</small></template>
              <template v-slot:edit="field">
                <div :class="{ 'kc-recomend': checkKeyConcept(field.data) }"> {{ field.data.name_eng }}
                  (<span v-for="(rs, index) in field.data.recommended_subjects" :key="rs.id"><span v-if="index != 0">,
                  </span>{{ rs.name_eng }}</span>)</div>
              </template>
            </unit-field-checkbox>
            <!-- Предметные концепции -->
            <unit-field-checkbox id="related_concepts" :fieldName="'related_concepts'" :fieldText="fieldText.related_concepts"
              :checkLine="true" :fieldData="interdisciplinaryUnit.related_concepts" :options="relatedConcepts" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field"><b>{{ field.data.name_eng }}</b><br><small>
                {{ field.data.description_eng }}</small></template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Концептуальное понимание -->
            <unit-field-text id="conceptual_understanding" :fieldName="'conceptual_understanding'"
              :fieldText="fieldText.conceptual_understanding" :fieldData="interdisciplinaryUnit.conceptual_understanding"
              @save="unitIDFieldSave" />
            <!-- Глобальный контекст -->
            <unit-field-radio id="global_context" :fieldName="'global_context'" :fieldText="fieldText.global_context"
              :fieldData="interdisciplinaryUnit.global_context" :options="globalContexts" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}<br>
                <small>{{ field.data.description_eng }}</small></template>
            </unit-field-radio>
            <!-- Линии исследования -->
            <unit-field-checkbox v-if="interdisciplinaryUnit.global_context" id="explorations" :fieldName="'explorations'" :fieldText="fieldText.explorations"
              :checkLine="true" :fieldData="interdisciplinaryUnit.explorations" :options="explorations" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Формулировка исследования -->
            <unit-field-text id="statement_inquiry" :fieldName="'statement_inquiry'" :fieldText="fieldText.statement_inquiry" 
            :fieldData="interdisciplinaryUnit.statement_inquiry" @save="unitIDFieldSave" />
            <!-- Исследовательские вопросы -->
            <unit-field-blocks id="inquiry_questions" :fieldName="'inquiry_questions'" :fieldText="fieldText.inquiry_questions"
              :defaultItem="defaultInQuestion" :fieldData="interdisciplinaryUnit.inquiry_questions" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="blocks-title"><span class="question-type">{{ field.data.type_text }}</span>{{ field.data.question }}</div>
                  <div class="question-line">Линия исследования: {{ field.data.line }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="my-2">
                  <textarea class="form-control mb-2" type="text" v-model="item.data.question"
                    placeholder="Исследовательский вопрос"></textarea>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <select id="subject" class="form-select mb-2" v-model="item.data.type">
                      <option :value="null">Выберите тип</option>
                      <option v-for="(op, i) in questionTypes" :key="i" :value="op.value">
                        {{ op.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-md">
                    <textarea class="form-control mb-2" type="text" v-model="item.data.line" rows="1"
                      placeholder="Линия исследования"></textarea>
                  </div>
                </div>
              </template>
            </unit-field-blocks>
            <!-- ОБРАЗОВАТЕЛЬНЫЕ ЦЕЛИ -->
            <div id="myp-objectives" class="myp-header">Образовательные цели</div>
            <!-- Общие цели -->
            <unit-field-checkbox id="aims" :fieldName="'aims'" :fieldText="fieldText.aims"
              :fieldData="interdisciplinaryUnit.aims" :options="aims" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Критерии оценки -->
            <unit-field-checkbox id="criteria" :fieldName="'criteria'" :fieldText="fieldText.criteria"
              :fieldData="interdisciplinaryUnit.criteria" :options="criteriaMYP" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.letter }}. {{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.letter }}. {{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Предметные цели -->
            <unit-field-checkbox-grouped id="strands" :fieldName="'strands'" :fieldText="fieldText.strands" :fieldGroup="'criterion'"
              :fieldData="interdisciplinaryUnit.strands" :options="strands" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <template v-slot:showGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:show="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
              <template v-slot:editGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:edit="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
            </unit-field-checkbox-grouped>
            <!-- Задания МДП -->
            <unit-field-text id="tasks" :fieldName="'tasks'" :fieldText="fieldText.tasks" 
            :fieldData="interdisciplinaryUnit.tasks" @save="unitIDFieldSave" />
            <!-- УЧЕБНАЯ ДЕЯТЕЛЬНОСТЬ И ОЦЕНИВАНИЕ -->
            <div id="myp-teaching-assessment" class="myp-header">Учебная деятельность и оценивание</div>
            <!-- Введение в МДП -->
            <unit-field-text id="introduction" :fieldName="'introduction'" :fieldText="fieldText.introduction" 
            :fieldData="interdisciplinaryUnit.introduction" @save="unitIDFieldSave" />
            <!-- Учебная деятельность -->
            <unit-field-text id="learning_teaching" :fieldName="'learning_teaching'" :fieldText="fieldText.learning_teaching" 
            :fieldData="interdisciplinaryUnit.learning_teaching" @save="unitIDFieldSave" />
            <!-- Текущее оценивание -->
            <unit-field-text id="formative_assessment" :fieldName="'formative_assessment'" :fieldText="fieldText.formative_assessment" 
            :fieldData="interdisciplinaryUnit.formative_assessment" @save="unitIDFieldSave" />
            <!-- Итоговое оценивание -->
            <unit-field-text id="summative_assessment" :fieldName="'summative_assessment'" :fieldText="fieldText.summative_assessment" 
            :fieldData="interdisciplinaryUnit.summative_assessment" @save="unitIDFieldSave" />
            <!-- Дифференциация -->
            <unit-field-text id="differentiation" :fieldName="'differentiation'" :fieldText="fieldText.differentiation" 
            :fieldData="interdisciplinaryUnit.differentiation" @save="unitIDFieldSave" />
            <!-- РЕФЛЕКСИЯ -->
            <div id="myp-reflections" class="myp-header">Рефлексия</div>
            <!-- Посты рефлексии перед началом юнита -->
            <unit-field-blocks id="reflections_prior" :fieldName="'reflections_prior'" :fieldText="fieldText.reflection_prior"
              :fieldData="interdisciplinaryUnit.reflections.filter(item => item.type == 'Prior')"
              :defaultItem="this.defaultReflection['postPrior']" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div>{{ field.data.post }}</div>
                  <div class="post-author">{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="my-2">
                  <textarea class="form-control mb-2" type="text" v-model="item.data.post"
                    placeholder="Напишите обратную связь"></textarea>
                </div>
              </template>
            </unit-field-blocks>
            <!-- Посты рефлексии во время юнита -->
            <unit-field-blocks id="reflections_during" :fieldName="'reflections_during'" :fieldText="fieldText.reflection_during"
              :fieldData="interdisciplinaryUnit.reflections.filter(item => item.type == 'During')"
              :defaultItem="this.defaultReflection['postDuring']" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div>{{ field.data.post }}</div>
                  <div class="post-author">{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="my-2">
                  <textarea class="form-control mb-2" type="text" v-model="item.data.post"
                    placeholder="Напишите обратную связь"></textarea>
                </div>
              </template>
            </unit-field-blocks>
            <!-- Посты рефлексии после юнита -->
            <unit-field-blocks id="reflections_after" :fieldName="'reflections_after'" :fieldText="fieldText.reflection_after"
              :fieldData="interdisciplinaryUnit.reflections.filter(item => item.type == 'After')"
              :defaultItem="this.defaultReflection['postAfter']" @save="unitIDFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div>{{ field.data.post }}</div>
                  <div class="post-author">{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="my-2">
                  <textarea class="form-control mb-2" type="text" v-model="item.data.post"
                    placeholder="Напишите обратную связь"></textarea>
                </div>
              </template>
            </unit-field-blocks>
          </div>
        </div>
        <div class="d-flex border-top mt-3">
          <button type="button" class="btn btn-danger ms-auto my-3" @click="showUnitModal">
            Удалить этот юнит
          </button>
        </div>
      </div>
    </transition>
    <modal-unit :modalId="'modalUnitDelete'" :modalTitle="modalTitle" :flagUnit="flagUnit" 
    @cancel="hideUnitModal" @delete="unitDelete">
      <div v-if="flagUnit.delete">
        <div>Вы действительно хотите удалить этот юнит?</div>
        <div class="border mt-2 p-2">
          <div class="idu-header">{{ interdisciplinaryUnit.title }}</div>
          <div>Год обучения: {{ interdisciplinaryUnit.class_year.year_ib }} ({{ interdisciplinaryUnit.class_year.year_rus }} класс)</div>
          <div>Предметы: 
            <span v-for="(un, index) in interdisciplinaryUnit.unitplan_myp" :key="un.id">
              {{ un.subject.name_rus }}<span v-if="++index !== interdisciplinaryUnit.unitplan_myp.length">,&nbsp;</span>
            </span>
          </div>
        </div>
      </div>
    </modal-unit>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex'
import Editor from '@tinymce/tinymce-vue';
import fieldTextIDU from '@/assets/fieldstext-idu.json'
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getKeyConcepts } from "@/hooks/unit/useKeyConcept";
import { getRelatedConcepts } from "@/hooks/unit/useRelatedConcept";
import { getGlobalContext } from "@/hooks/unit/useGlobalContext";
import { getExplorations } from "@/hooks/unit/useExploration";
import { getStrands } from "@/hooks/unit/useStrand";
import { getATLSkills } from "@/hooks/unit/useATLSkills";
import { getAims } from "@/hooks/unit/useAim";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";
import { getInterdisciplinaryUnit, updateInterdisciplinaryUnit, deleteInterdisciplinaryUnit } from "@/hooks/unit/useInterdisciplinaryUnit";
import { getUnitListMYP } from "@/hooks/unit/useUnitMYP";

export default {
  name: 'UnitIDView',
  components: {
    'editor': Editor
  },
  setup(props) {
    const { years, fetchGetClassYears } = getClassYears();
    const { keyConcepts, fetchGetKeyConcepts } = getKeyConcepts();
    const { relatedConcepts, fetchGetRelatedConcepts } = getRelatedConcepts();
    const { globalContexts, fetchGetGlobalContexts } = getGlobalContext();
    const { explorations, fetchGetExplorations } = getExplorations();
    const { aims, fetchGetAims } = getAims();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();
    const { strands, fetchGetStrands } = getStrands();
    const { atlSkills, fetchGetATLSkills } = getATLSkills();
    const { interdisciplinaryUnit, isUnitIDLoading, fetchGetInterdisciplinaryUnit } = getInterdisciplinaryUnit();
    const { updatedInterdisciplinaryUnit, fetchUpdateInterdisciplinaryUnit } = updateInterdisciplinaryUnit();
    const { fetchDeleteInterdisciplinaryUnit } = deleteInterdisciplinaryUnit();
    const { unitListMYP, fetchGetUnitListMYP } = getUnitListMYP();
    return {
      years, fetchGetClassYears,
      keyConcepts, fetchGetKeyConcepts,
      relatedConcepts, fetchGetRelatedConcepts,
      globalContexts, fetchGetGlobalContexts,
      explorations, fetchGetExplorations,
      aims, fetchGetAims,
      strands, fetchGetStrands,
      criteriaMYP, fetchGetCriteriaMYP,
      atlSkills, fetchGetATLSkills,
      interdisciplinaryUnit, isUnitIDLoading, fetchGetInterdisciplinaryUnit,
      updatedInterdisciplinaryUnit, fetchUpdateInterdisciplinaryUnit,
      fetchDeleteInterdisciplinaryUnit,
      unitListMYP, fetchGetUnitListMYP
    }
  },
  data() {
    return {
      fieldText: fieldTextIDU,
      questionTypes: [
        { name: "Фактический", value: 'Factual' },
        { name: "Концептуальный", value: 'Conceptual' },
        { name: "Дискуссионный", value: 'Debatable' },
      ],
      defaultInQuestion: {
        type: null,
      },
      defaultReflection: {
        postPrior: {
          type: 'Prior',
        },
        postDuring: {
          type: 'During',
        },
        postAfter: {
          type: 'After',
        },
      },
      modalUnitDelete: null,
      modalTitle: '',
      flagUnit: {},
    }
  },
  methods: {
    unitFieldEdit(field) {
      switch(field) {
        case 'class_year':
          this.fetchGetClassYears({ program: 'MYP' });
          break;
        case 'key_concepts':
          this.fetchGetKeyConcepts();
          break;
        case 'related_concepts':
          this.fetchGetRelatedConcepts({ subjects: this.interdisciplinaryUnit.unitplan_myp.map(item => item.subject.id)});
          break;
        case 'global_context':
         this.fetchGetGlobalContexts();
          break;
        case 'explorations':
         this.fetchGetExplorations({ gcontext: this.interdisciplinaryUnit.global_context.id });
          break;
        case 'aims':
          this.fetchGetAims({ group: 10 });
          break;
        case 'criteria':
          this.fetchGetCriteriaMYP({ group: 10 })
          break;
        case 'strands':
          this.fetchGetStrands({ group: 10, criteria: this.interdisciplinaryUnit.criteria.map(item => item.id)});
          break;
        case 'reflections_prior':
          this.defaultReflection.postPrior['author_id'] = this.authUser.teacher.id;
          break;
        case 'reflections_during':
          this.defaultReflection.postDuring['author_id'] = this.authUser.teacher.id;
          break;
        case 'reflections_after':
          this.defaultReflection.postAfter['author_id'] = this.authUser.teacher.id;
          break;
        case 'unitplan_myp':
          this.fetchGetUnitListMYP({ year: this.interdisciplinaryUnit.class_year_id, interdisciplinary: this.interdisciplinaryUnit.id });
          break;
      }
    },
    unitIDFieldSave(unit) {
      console.log('Сохранение междисциплинарного юнита: ', unit);
      this.fetchUpdateInterdisciplinaryUnit(this.$route.params.id, unit).finally(() => {
        this.interdisciplinaryUnit = { ...this.updatedInterdisciplinaryUnit }
      })
    },
    // Проверка ключевого концепта в качестве рекомендованного в предметной группе
    checkKeyConcept(field) {
      return field.recommended_subjects.filter(item => this.interdisciplinaryUnit.unitplan_myp.map(item => item.subject.group_ib.id).includes(item.id)).length;
    },
    // Получить критерий по ID из данных юнита
    getCriteriaByID(id) {
      return this.interdisciplinaryUnit.criteria.find(item => item.id == id)
    },
    checkField(field, type=null) {
      if (Array.isArray(this.interdisciplinaryUnit[field])) {
        if (type) {
          return Boolean(this.interdisciplinaryUnit[field].filter(item => item.type == type).length) ? 'field-check' : null
        }
        return Boolean(this.interdisciplinaryUnit[field].length) ? 'field-check' : null
      } else {
        return Boolean(this.interdisciplinaryUnit[field]) ? 'field-check' : null
      }
    },
    showUnitModal() {
      this.modalTitle = 'Удаление междисциплинарного юнита';
      this.flagUnit.delete = true;
      this.modalUnitDelete.show()
    },
    hideUnitModal() {
      this.flagUnit.delete = false;
      this.modalUnitDelete.hide()
    },
    unitDelete() {
      console.log('Удаление междисциплинарного юнита');
      this.fetchDeleteInterdisciplinaryUnit(this.$route.params.id).finally(() => {
        this.flagUnit.delete = false;
        this.modalUnitDelete.hide();
        this.$router.push(`/myp`);
      })
    },
  },
  mounted() {
    this.modalUnitDelete = new Modal('#modalUnitDelete', { backdrop: 'static' });
    this.fetchGetInterdisciplinaryUnit(this.$route.params.id);
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
}
</script>

<style scoped>
@import '@/assets/css/field.css';

.text-block {
  white-space: pre-wrap;
}
.myp-sidebar {
  max-width: 300px;
}
.navbar-myp {
  font-size: 0.9em;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: scroll;
  -ms-overflow-style: none;
  scrollbar-width: none; 
}
@media (max-width: 576px) {
  .myp-sidebar {
    max-width: 100%;
  }
  .navbar-myp {
    height: inherit;
  }
}

.navbar-myp::-webkit-scrollbar {
  display: none;
}
.myp-header {
  margin-bottom: 20px;
  font-size: 2em;
}
.myp-header:not(:first-of-type) {
  margin-top: 20px;
}
.unit-wrapper {
  padding: 5px;
}
.unit-wrapper:hover {
  cursor: pointer;
  background: #CFCFCF;
  border-radius: 5px;
  transition: 0.5s;
}
.kc-recomend {
  color: rgb(6, 134, 27);
  font-weight: bold;
}
.nav-link {
  padding: 0;
  margin: 0;
  font-weight: 400;
}
.myp-group {
  margin: 5px 0;
  font-size: 1.2em;
}
.myp-field {
  margin-left: 20px;
  margin-right: 5px;
  padding: 5px 0;
  position: relative;
}
.myp-field:before {
  content: "";
  position: absolute;
  left: -20px;
  top: 8px;
  float: left;
  width: 15px;
  height: 15px;
  margin-right: 5px;
  background: url('@/assets/img/check-no.png') no-repeat 50% / 100%;
}
.field-check:before {
  background: url('@/assets/img/check-yes.png') no-repeat 50% / 100%;
}
.blocks-wrapper {
  display: flex;
  flex-wrap: wrap;
  width: 100%
}
.blocks-title {
  font-weight: 700;
  margin-right: 10px;
  flex-basis: 100%;
}
.question-type {
  background-color: green;
  padding: 1px 5px;
  border-radius: 5px;
  color: #fff;
  font-size: 0.8em;
  order: -1;
  margin-right: 5px;
}
.question-line {
  flex-basis: 100%;
}

.post-author {
  text-align: right;
  flex-basis: 100%;
  font-style: italic;
}

</style>