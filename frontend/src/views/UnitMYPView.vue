<template>
  <div>
    <base-header>
      <template v-slot:link><div @click="$router.push(`/myp`)"  class="link">Вернуться к списку юнитов</div></template>
      <template v-slot:header>MYP: Работа с предметным юнитом</template>
    </base-header>
    <transition name="fade">
      <div class="row" v-if="!isUnitLoading">
        <div class="col-sm myp-sidebar">
          <!-- Процент заполнения юнита -->
          <div>Заполнение юнита</div>
          <div class="progress" style="height: 20px;">
            <div class="progress-bar" role="progressbar" :style="`width: ${unitMYP.fullness}%`" :aria-valuenow="unitMYP.fullness" aria-valuemin="0" aria-valuemax="100">{{ unitMYP.fullness }}%</div>
          </div>
          <nav id="navbar-myp" class="navbar-myp">
            <nav class="nav nav-pills flex-column">
              <a class="nav-link myp-group" href="#myp-base">Основная информация</a>
              <a class="nav-link myp-group" href="#myp-inquiry">Исследование</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('key_concepts')" href="#key_concepts">Ключевые концепты</a>
                <a class="nav-link myp-field cheking" :class="checkField('related_concepts')" href="#related_concepts">Предметные концепты</a>
                <a class="nav-link myp-field cheking" :class="checkField('conceptual_understanding')" href="#conceptual_understanding">Концептуальное понимание</a>
                <a class="nav-link myp-field cheking" :class="checkField('global_context')" href="#global_context">Глобальный контекст</a>
                <a class="nav-link myp-field cheking" :class="checkField('explorations')" href="#explorations">Линии исследования</a>
                <a class="nav-link myp-field cheking" :class="checkField('statement_inquiry')" href="#statement_inquiry">Формулировка исследования</a>
                <a class="nav-link myp-field cheking" :class="checkField('inquiry_questions')" href="#inquiry_questions">Исследовательские вопросы</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-objectives">Образовательные цели</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('aims')" href="#aims">Общие цели</a>
                <a class="nav-link myp-field cheking" :class="checkField('criteria')" href="#criteria">Критерии оценивания</a>
                <a class="nav-link myp-field cheking" :class="checkField('strands')" href="#strands">Цели предметной группы</a>
                <a class="nav-link myp-field cheking" :class="checkField('content')" href="#content">Содержание</a>
                <a class="nav-link myp-field cheking" :class="checkField('skills')" href="#skills">Умения</a>
                <a class="nav-link myp-field cheking" :class="checkField('atl_mapping')" href="#atl_mapping">Карта ATL</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-profile">Профиль студента</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('learner_profile')" href="#learner_profile">Профиль студента IB</a>
                <a class="nav-link myp-field cheking" :class="checkField('international_mindedness')" href="#international_mindedness">Межкультурное понимание</a>
                <a class="nav-link myp-field cheking" :class="checkField('academic_integrity')" href="#academic_integrity">Академическая честность</a>
                <a class="nav-link myp-field cheking" :class="checkField('language_development')" href="#language_development">Языковое развитие</a>
                <a class="nav-link myp-field cheking" :class="checkField('infocom_technology')" href="#infocom_technology">Использование средств ИКТ</a>
                <a class="nav-link myp-field cheking" :class="checkField('service_as_action')" href="#service_as_action">Служение как действие</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-assessment">Оценивание</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('formative_assessment')" href="#formative_assessment">Текущее оценивание</a>
                <a class="nav-link myp-field cheking" :class="checkField('summative_assessment_task')" href="#summative_assessment_task">Итоговое оценивание (задания)</a>
                <a class="nav-link myp-field cheking" :class="checkField('summative_assessment_soi')" href="#summative_assessment_soi">Итоговое оценивание (взаимосвязь с
                  исследовательским утверждением)</a>
                <a class="nav-link myp-field cheking" :class="checkField('peer_self_assessment')" href="#peer_self_assessment">Взаимное и самооценивание</a>
                <a class="nav-link myp-field cheking" :class="checkField('standardization_moderation')" href="#standardization_moderation">Стандартизация и модерация</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-teaching">Стратегии преподавания</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('prior_experiences')"  href="#prior_experiences">Предыдущий опыт обучения</a>
                <a class="nav-link myp-field cheking" :class="checkField('learning_experiences')" href="#learning_experiences">Учебная деятельность</a>
                <a class="nav-link myp-field cheking" :class="checkField('teaching_strategies')" href="#teaching_strategies">Стратегии преподавания</a>
                <a class="nav-link myp-field cheking" :class="checkField('student_expectations')" href="#student_expectations">Ожидания студентов</a>
                <a class="nav-link myp-field cheking" :class="checkField('feedback')" href="#feedback">Обратная связь</a>
                <a class="nav-link myp-field cheking" :class="checkField('differentiation')" href="#differentiation">Дифференциация</a>
                <a class="nav-link myp-field cheking" :class="checkField('resources')" href="#resources">Ресурсы</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-reflections">Рефлексия</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field cheking" :class="checkField('reflections', type='Prior')"  href="#reflections_prior">До начала изучения</a>
                <a class="nav-link myp-field cheking" :class="checkField('reflections', type='During')" href="#reflections_during">В процессе изучения юнита</a>
                <a class="nav-link myp-field cheking" :class="checkField('reflections', type='After')" href="#reflections_after">По окончании изучения юнита</a>
              </nav>
            </nav>
          </nav>
        </div>
        <div class="col-sm">
          <div data-bs-spy="scroll" data-bs-target="#navbar-myp" data-bs-smooth-scroll="true" tabindex="0">
            <!-- МЕЖДИСЦИПЛИНАРНЫЙ ЮНИТ -->
            <div v-if="unitMYP.interdisciplinary">
              <div id="myp-base" class="myp-header"><h2>Это междисциплинарный юнит</h2></div>
              <div class="myp-interdisciplinary" @click="$router.push(`/myp/idu/${unitMYP.interdisciplinary.id}`)">
                <div class="idu-header">{{ unitMYP.interdisciplinary.title }}</div>
                <div>Предметы: 
                  <span v-for="(un, index) in unitMYP.interdisciplinary.unitplan_myp" :key="un.id">
                  {{ un.subject.name_rus }}<span v-if="++index !== unitMYP.interdisciplinary.unitplan_myp.length">,&nbsp;</span>
                </span></div>
              </div>
              <div class="d-flex">
                <button class="idu-btn-delete" @click="showUnitIDUModal">Удалить связь с МДП</button>
              </div>
            </div>
            <!-- ОСНОВНАЯ ИНФОРМАЦИЯ -->
            <div id="myp-base" class="myp-header"><h2>Основная информация</h2></div>
            <!-- Название юнита -->
            <unit-field-string id="title" :fieldName="'title'" :fieldText="fieldText.title" :fieldData="unitMYP.title"
              @save="unitFieldSave" />
            <div class="row">
              <div class="col-md-5">
                <!-- Количество часов -->
                <unit-field-string id="hours" :fieldName="'hours'" :fieldText="fieldText.hours" :fieldData="unitMYP.hours"
                  @save="unitFieldSave" />
              </div>
              <div class="col-md">
                <!-- Год обучения -->
                <unit-field-select id="class_year" :fieldName="'class_year'" :fieldText="fieldText.class_year"
                  :fieldData="unitMYP.class_year" :options="years" @save="unitFieldSave" @edit="unitFieldEdit">
                  <template v-slot:show="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
                  <template v-slot:edit="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
                </unit-field-select>
              </div>
            </div>
            <div class="row">
              <div class="col-md">
                <!-- Предмет -->
                <unit-field-select id="subject" :fieldName="'subject'" :fieldText="fieldText.subject"
                  :fieldData="unitMYP.subject" :options="subjects" @save="unitFieldSave" @edit="unitFieldEdit">
                  <template v-slot:show="field">{{ field.data.name_rus }} ({{ field.data.group_ib.name_eng }})</template>
                  <template v-slot:edit="field">{{ field.data.name_rus }} ({{ field.data.group_ib.name_eng }})</template>
                </unit-field-select>
              </div>
              <div class="col-md-6">
                <!-- Уровень изучения предмета -->
                <unit-field-select v-if="unitMYP.subject" id="level" :fieldName="'level'" :fieldText="fieldText.level"
                  :fieldData="unitMYP.level" :options="levels" @save="unitFieldSave" @edit="unitFieldEdit">
                  <template v-slot:show="field">{{ field.data.name_eng }}</template>
                  <template v-slot:edit="field">{{ field.data.name_eng }}</template>
                </unit-field-select>
              </div>
            </div>
            <!-- Авторы юнита -->
            <unit-field-checkbox-search id="authors" :fieldName="'authors'" :fieldText="fieldText.authors" :fieldSearch="'last_name'"
              :fieldData="unitMYP.authors" :options="teachers" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.last_name }} {{ field.data.first_name }} {{ field.data.middle_name }}</template>
              <template v-slot:edit="field">{{ field.data.last_name }} {{ field.data.first_name }} {{ field.data.middle_name }}</template>
            </unit-field-checkbox-search>
            <!-- ИССЛЕДОВАНИЕ -->
            <div id="myp-inquiry" class="myp-header"><h2>Исследование</h2></div>
            <!-- Ключевые концепции -->
            <unit-field-checkbox id="key_concepts" :fieldName="'key_concepts'" :fieldText="fieldText.key_concepts"
              :fieldData="unitMYP.key_concepts" :options="keyConcepts" @save="unitFieldSave" @edit="unitFieldEdit">
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
              :checkLine="true" :fieldData="unitMYP.related_concepts" :options="relatedConcepts" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field"><b>{{ field.data.name_eng }}</b><br><small>
                {{ field.data.description_eng }}</small></template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Концептуальное понимание -->
            <unit-field-text id="conceptual_understanding" :fieldName="'conceptual_understanding'"
              :fieldText="fieldText.conceptual_understanding" :fieldData="unitMYP.conceptual_understanding"
              @save="unitFieldSave" />
            <!-- Глобальный контекст -->
            <unit-field-radio id="global_context" :fieldName="'global_context'" :fieldText="fieldText.global_context"
              :fieldData="unitMYP.global_context" :options="globalContexts" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}<br>
                <small>{{ field.data.description_eng }}</small></template>
            </unit-field-radio>
            <!-- Линии исследования -->
            <unit-field-checkbox v-if="unitMYP.global_context" id="explorations" :fieldName="'explorations'" :fieldText="fieldText.explorations"
              :checkLine="true" :fieldData="unitMYP.explorations" :options="explorations" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Формулировка исследования -->
            <unit-field-text id="statement_inquiry" :fieldName="'statement_inquiry'" :fieldText="fieldText.statement_inquiry" 
            :fieldData="unitMYP.statement_inquiry" @save="unitFieldSave" />
            <!-- Исследовательские вопросы -->
            <unit-field-blocks id="inquiry_questions" :fieldName="'inquiry_questions'" :fieldText="fieldText.inquiry_questions"
            :defaultItem="defaultInQuestion" :fieldData="unitMYP.inquiry_questions" @save="unitFieldSave" @edit="unitFieldEdit">
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
            <div id="myp-objectives" class="myp-header"><h2>Образовательные цели</h2></div>
            <!-- Общие цели -->
            <unit-field-checkbox id="aims" :fieldName="'aims'" :fieldText="fieldText.aims"
              :fieldData="unitMYP.aims" :options="aims" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Критерии оценки -->
            <unit-field-checkbox id="criteria" :fieldName="'criteria'" :fieldText="fieldText.criteria"
              :fieldData="unitMYP.criteria" :options="criteriaMYP" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.letter }}. {{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.letter }}. {{ field.data.name_eng }}</template>
            </unit-field-checkbox>
            <!-- Предметные цели -->
            <unit-field-checkbox-grouped id="strands" :fieldName="'strands'" :fieldText="fieldText.strands" :fieldGroup="'criterion'"
              :fieldData="unitMYP.strands" :options="strands" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:showGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:show="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
              <template v-slot:editGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:edit="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
            </unit-field-checkbox-grouped>
            <!-- Содержание -->
            <unit-field-text id="content" :fieldName="'content'" :fieldText="fieldText.content" :fieldData="unitMYP.content"
              @save="unitFieldSave" />
            <!-- Умения -->
            <unit-field-text id="skills" :fieldName="'skills'" :fieldText="fieldText.skills" :fieldData="unitMYP.skills"
              @save="unitFieldSave" />
            <!-- Карта развития ATL-навыков -->
            <unit-field-blocks id="atl_mapping" :fieldName="'atl_mapping'" :fieldText="fieldText.atl_mapping"
            :defaultItem="defaultATLSkill" :fieldData="unitMYP.atl_mapping" @save="unitFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="blocks-title">ATL: {{ field.data.atl.name_eng }}</div>
                  <div>Objective: {{ field.data.strand.criterion.letter }} {{ field.data.strand.letter_i }}. {{ field.data.strand.name_eng }}</div>
                  <div style="font-style: italic;">{{ field.data.action }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="row">
                  <div class="col-md">
                    <select id="subject" class="form-select mb-2" v-model="item.data.atl_id">
                      <option :value="null">Выберите навык ATL</option>
                      <option v-for="(op, i) in atlSkills" :key="i" :value="op.id">
                        {{ op.name_eng }} ({{ op.cluster.name_eng }})
                      </option>
                    </select>
                  </div>
                  <div class="col-md">
                    <select id="subject" class="form-select mb-2" v-model="item.data.strand_id">
                      <option :value="null">Выберите образовательную цель</option>
                      <option v-for="(op, i) in unitMYP.strands" :key="i" :value="op.id">
                        {{ op.criterion.letter }} {{ op.letter_i }}. {{ op.name_eng }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="my-2">
                    <textarea class="form-control mb-2" type="text" v-model="item.data.action"
                      placeholder="Действия"></textarea>
                  </div>
              </template>
            </unit-field-blocks>
            <!-- Профиль студента -->
            <div id="myp-profile" class="myp-header"><h2>Профиль студента</h2></div>
            <!-- Таблица развития профиля студента IB -->
            <unit-field-blocks id="learner_profile" :fieldName="'learner_profile'" :fieldText="fieldText.learner_profile"
            :defaultItem="defaultProfile" :fieldData="unitMYP.learner_profile" @save="unitFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="blocks-title">{{ field.data.profile.name_eng }}</div>
                  <div>{{ field.data.description }}</div>
                </div>
              </template>
              <!-- Слот для формы редактирования записей -->
              <template v-slot:form="item">
                <div class="row">
                  <div class="col-md">
                    <select id="subject" class="form-select mb-2" v-model="item.data.profile_id">
                      <option :value="null">Выберите IB Profile</option>
                      <option v-for="(op, i) in ibProfiles" :key="i" :value="op.id">
                        {{ op.name_eng }} 
                      </option>
                    </select>
                  </div>
                </div>
                <div class="my-2">
                    <textarea class="form-control mb-2" type="text" v-model="item.data.description"
                      placeholder="Описание развития профиля"></textarea>
                  </div>
              </template>
            </unit-field-blocks>
            <!-- Межкультурное понимание -->
            <unit-field-text id="international_mindedness" :fieldName="'international_mindedness'" :fieldText="fieldText.international_mindedness" :fieldData="unitMYP.international_mindedness"
              @save="unitFieldSave" />
            <!-- Академическая честность -->
            <unit-field-text id="academic_integrity" :fieldName="'academic_integrity'" :fieldText="fieldText.academic_integrity" :fieldData="unitMYP.academic_integrity"
              @save="unitFieldSave" />
            <!-- Языковое развитие -->
            <unit-field-text id="language_development" :fieldName="'language_development'" :fieldText="fieldText.language_development" :fieldData="unitMYP.language_development"
              @save="unitFieldSave" />
            <!-- Использование средств ИКТ -->
            <unit-field-text id="infocom_technology" :fieldName="'infocom_technology'" :fieldText="fieldText.infocom_technology" :fieldData="unitMYP.infocom_technology"
              @save="unitFieldSave" />
            <!-- Служение как действие -->
            <unit-field-text id="service_as_action" :fieldName="'service_as_action'" :fieldText="fieldText.service_as_action" :fieldData="unitMYP.service_as_action"
              @save="unitFieldSave" />
            <!-- ОЦЕНИВАНИЕ -->
            <div id="myp-assessment" class="myp-header"><h2>Оценивание</h2></div>
            <!-- Текущее оценивание -->
            <unit-field-text id="formative_assessment" :fieldName="'formative_assessment'" :fieldText="fieldText.formative_assessment" :fieldData="unitMYP.formative_assessment"
              @save="unitFieldSave" />
            <!-- Итоговое оценивание (задания) -->
            <unit-field-text id="summative_assessment_task" :fieldName="'summative_assessment_task'" :fieldText="fieldText.summative_assessment_task" :fieldData="unitMYP.summative_assessment_task"
              @save="unitFieldSave" />
            <!-- Итоговое оценивание (взаимосвязь с исследовательским утверждением) -->
            <unit-field-text id="summative_assessment_soi" :fieldName="'summative_assessment_soi'" :fieldText="fieldText.summative_assessment_soi" :fieldData="unitMYP.summative_assessment_soi"
              @save="unitFieldSave" />
            <!-- Взаимное и самооценивание -->
            <unit-field-text id="peer_self_assessment" :fieldName="'peer_self_assessment'" :fieldText="fieldText.peer_self_assessment" :fieldData="unitMYP.peer_self_assessment"
              @save="unitFieldSave" />
            <!-- Стандартизация и модерация -->
            <unit-field-text id="standardization_moderation" :fieldName="'standardization_moderation'" :fieldText="fieldText.standardization_moderation" :fieldData="unitMYP.standardization_moderation"
              @save="unitFieldSave" />
            <!-- СТРАТЕГИИ ПРЕПОДАВАНИЯ -->
            <div id="myp-teaching" class="myp-header"><h2>Стратегии преподавания</h2></div>
            <!-- Предыдущий опыт обучения -->
            <unit-field-text id="prior_experiences" :fieldName="'prior_experiences'" :fieldText="fieldText.prior_experiences" :fieldData="unitMYP.prior_experiences"
              @save="unitFieldSave" />
            <!-- Учебная деятельность -->
            <unit-field-text id="learning_experiences" :fieldName="'learning_experiences'" :fieldText="fieldText.learning_experiences" :fieldData="unitMYP.learning_experiences"
              @save="unitFieldSave" />
            <!-- Стратегии преподавания -->
            <unit-field-text id="teaching_strategies" :fieldName="'teaching_strategies'" :fieldText="fieldText.teaching_strategies" :fieldData="unitMYP.teaching_strategies"
              @save="unitFieldSave" />
            <!-- Ожидания студентов -->
            <unit-field-text id="student_expectations" :fieldName="'student_expectations'" :fieldText="fieldText.student_expectations" :fieldData="unitMYP.student_expectations"
              @save="unitFieldSave" />
            <!-- Обратная связь -->
            <unit-field-text id="feedback" :fieldName="'feedback'" :fieldText="fieldText.feedback" :fieldData="unitMYP.feedback"
              @save="unitFieldSave" />
            <!-- Дифференциация -->
            <unit-field-text id="differentiation" :fieldName="'differentiation'" :fieldText="fieldText.differentiation" :fieldData="unitMYP.differentiation"
              @save="unitFieldSave" />
            <!-- Ресурсы -->
            <unit-field-text id="resources" :fieldName="'resources'" :fieldText="fieldText.resources" :fieldData="unitMYP.resources"
              @save="unitFieldSave" />
            <!-- РЕФЛЕКСИЯ -->
            <div id="myp-reflections" class="myp-header"><h2>Рефлексия</h2></div>
            <!-- Посты рефлексии перед началом юнита -->
            <unit-field-blocks id="reflections_prior" :fieldName="'reflections_prior'" :fieldText="fieldText.reflection_prior"
              :fieldData="unitMYP.reflections.filter(item => item.type == 'Prior')"
              :defaultItem="this.defaultReflection['postPrior']" @save="unitFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="post-text">{{ field.data.post }}</div>
                  <div>{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
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
              :fieldData="unitMYP.reflections.filter(item => item.type == 'During')"
              :defaultItem="this.defaultReflection['postDuring']" @save="unitFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="post-text">{{ field.data.post }}</div>
                  <div>{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
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
              :fieldData="unitMYP.reflections.filter(item => item.type == 'After')"
              :defaultItem="this.defaultReflection['postAfter']" @save="unitFieldSave" @edit="unitFieldEdit">
              <!-- Слот для блоков показа записей -->
              <template v-slot:show="field">
                <div class="blocks-wrapper">
                  <div class="post-text">{{ field.data.post }}</div>
                  <div>{{ field.data.author.first_name }} {{ field.data.author.middle_name }} {{ field.data.author.last_name }}</div>
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
      <!-- Модальное окно с формой удаления юнита -->
      <modal-unit :modalId="'modalUnitDelete'" :modalTitle="modalTitle" :flagUnit="flagUnit" 
      @cancel="hideUnitModal" @delete="unitDelete">
        <div v-if="flagUnit.delete">
          <div>Вы действительно хотите удалить этот юнит?</div>
          <div class="border mt-2 p-2">
            <div class="idu-header"><h4>{{ unitMYP.title }}</h4></div>
            <div>Год обучения: {{ unitMYP.class_year.year_ib }} ({{ unitMYP.class_year.year_rus }} класс)</div>
            <div>Предмет: {{ unitMYP.subject.name_rus }}</div>
            <div>Учителя: 
              <span v-for="(teacher, index) in unitMYP.authors" :key="teacher.id">
              {{ teacher.first_name }} {{ teacher.middle_name }} {{ teacher.last_name }}<span v-if="++index !== unitMYP.authors.length">,&nbsp;</span>
              </span>
            </div>
          </div>
        </div>
      </modal-unit>
      <!-- Модальное окно с формой удаления МДП -->
      <modal-unit :modalId="'modalUnitIDUDelete'" :modalTitle="modalTitle" :flagUnit="flagUnitIDU" 
      @cancel="hideUnitIDUModal" @delete="deleteIDURelation">
        <div v-if="flagUnitIDU.delete">
          <div>Вы действительно хотите удалить связь с междисциплинарным юнитом?</div>
          <div class="border mt-2 p-2">
            <div class="idu-header"><h4>{{ unitMYP.interdisciplinary.title }}</h4></div>
            <div>Предметы: 
              <span v-for="(un, index) in unitMYP.interdisciplinary.unitplan_myp" :key="un.id">
              {{ un.subject.name_rus }}<span v-if="++index !== unitMYP.interdisciplinary.unitplan_myp.length">,&nbsp;</span>
            </span></div>
          </div>
        </div>
      </modal-unit>
    </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex'
import Editor from '@tinymce/tinymce-vue';
import fieldText from '@/assets/fieldstext.json'
import { getUnitMYP, updateUnitMYP, deleteUnitMYP } from "@/hooks/unit/useUnitMYP";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getLevels } from "@/hooks/unit/useLevel";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getTeachers } from "@/hooks/user/useUser";
import { getKeyConcepts } from "@/hooks/unit/useKeyConcept";
import { getRelatedConcepts } from "@/hooks/unit/useRelatedConcept";
import { getGlobalContext } from "@/hooks/unit/useGlobalContext";
import { getExplorations } from "@/hooks/unit/useExploration";
import { getStrands } from "@/hooks/unit/useStrand";
import { getATLSkills } from "@/hooks/unit/useATLSkills";
import { getAims } from "@/hooks/unit/useAim";
import { getIBProfiles } from "@/hooks/unit/useIBProfile";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";
import { getInterdisciplinaryUnits } from "@/hooks/unit/useInterdisciplinaryUnit";

export default {
  name: 'UnitMYPView',
  components: {
    'editor': Editor
  },
  setup(props) {
    const { unitMYP, isUnitLoading, fetchGetUnitMYP } = getUnitMYP();
    const { updatedUnitMYP, fetchUpdateUnitMYP } = updateUnitMYP();
    const { fetchDeleteUnitMYP } = deleteUnitMYP();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { levels, fetchGetLevels } = getLevels();
    const { years, fetchGetClassYears } = getClassYears();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    const { keyConcepts, fetchGetKeyConcepts } = getKeyConcepts();
    const { relatedConcepts, fetchGetRelatedConcepts } = getRelatedConcepts();
    const { globalContexts, fetchGetGlobalContexts } = getGlobalContext();
    const { explorations, fetchGetExplorations } = getExplorations();
    const { aims, fetchGetAims } = getAims();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();
    const { strands, fetchGetStrands } = getStrands();
    const { atlSkills, fetchGetATLSkills } = getATLSkills();
    const { ibProfiles, fetchGetIBProfiles } = getIBProfiles();
    const { interdisciplinaryUnits, fetchGetInterdisciplinaryUnits } = getInterdisciplinaryUnits();
    return {
      unitMYP, isUnitLoading, fetchGetUnitMYP,
      updatedUnitMYP, fetchUpdateUnitMYP, fetchDeleteUnitMYP,
      years, fetchGetClassYears,
      teachers, isTeacherLoading, fetchGetTeachers,
      keyConcepts, fetchGetKeyConcepts,
      relatedConcepts, fetchGetRelatedConcepts,
      globalContexts, fetchGetGlobalContexts,
      explorations, fetchGetExplorations,
      aims, fetchGetAims,
      strands, fetchGetStrands,
      subjects, fetchGetSubjects,
      levels, fetchGetLevels,
      criteriaMYP, fetchGetCriteriaMYP,
      atlSkills, fetchGetATLSkills,
      ibProfiles, fetchGetIBProfiles,
      interdisciplinaryUnits, fetchGetInterdisciplinaryUnits,
    }
  },
  data() {
    return {
      fieldText: fieldText,
      questionTypes: [
        { name: "Фактический", value: 'Factual' },
        { name: "Концептуальный", value: 'Conceptual' },
        { name: "Дискуссионный", value: 'Debatable' },
      ],
      defaultInQuestion: {
        type: null,
      },
      defaultATLSkill: {
        atl_id: null,
        strand_id: null,
      },
      defaultProfile: {
        profile_id: null,
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
      modalUnitIDUDelete: null,
      flagUnit: {},
      flagUnitIDU: {},
      modalTitle: '',
    }
  },
  methods: {
    unitFieldEdit(field) {
      switch(field) {
        case 'subject':
          this.fetchGetSubjects({ program: 'MYP' });
          break;
        case 'level':
          this.fetchGetLevels({ subject: this.unitMYP.subject.id})
          break;
        case 'authors':
          this.fetchGetTeachers();
          break;
        case 'class_year':
          this.fetchGetClassYears({ program: 'MYP' });
          break;
        case 'key_concepts':
          this.fetchGetKeyConcepts();
          break;
        case 'related_concepts':
          this.fetchGetRelatedConcepts({ subject: this.unitMYP.subject.id });
          break;
        case 'global_context':
         this.fetchGetGlobalContexts();
          break;
        case 'explorations':
         this.fetchGetExplorations({ gcontext: this.unitMYP.global_context.id });
          break;
        case 'aims':
          this.fetchGetAims({ subject: this.unitMYP.subject.id });
          break;
        case 'criteria':
          this.fetchGetCriteriaMYP({ subject: this.unitMYP.subject.id })
          break;
        case 'strands':
          this.fetchGetStrands({ subject: this.unitMYP.subject.id, criteria: this.unitMYP.criteria.map(item => item.id)});
          break;
        case 'atl_mapping':
          this.fetchGetATLSkills();
          break;
        case 'learner_profile':
          this.fetchGetIBProfiles();
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
        case 'interdisciplinary':
          this.fetchGetInterdisciplinaryUnits({ class_year: this.unitMYP.class_year.id });
          break;
      }
    },
    unitFieldSave(unit) {
      console.log('Сохранение юнита: ', unit);
      this.fetchUpdateUnitMYP(this.$route.params.id, unit).finally(() => {
        this.unitMYP = { ...this.updatedUnitMYP }
      })
    },
    // Проверка ключевого концепта в качестве рекомендованного в предметной группе
    checkKeyConcept(field) {
      return field.recommended_subjects.filter(item => this.unitMYP.subject.group_ib.id == item.id).length;
    },
    // Получить критерий по ID из данных юнита
    getCriteriaByID(id) {
      return this.unitMYP.criteria.find(item => item.id == id)
    },
    checkField(field, type=null) {
      if (Array.isArray(this.unitMYP[field])) {
        if (type) {
          return Boolean(this.unitMYP[field].filter(item => item.type == type).length) ? 'field-check' : null
        }
        return Boolean(this.unitMYP[field].length) ? 'field-check' : null
      } else {
        return Boolean(this.unitMYP[field]) ? 'field-check' : null
      }
    },
    showUnitModal() {
      this.modalTitle = 'Удаление текущего юнита';
      this.flagUnit.delete = true;
      this.modalUnitDelete.show()
    },
    hideUnitModal() {
      this.flagUnit.delete = false;
      this.modalUnitDelete.hide()
    },
    showUnitIDUModal() {
      this.modalTitle = 'Удаление междисциплинарной связи';
      this.flagUnitIDU.delete = true;
      this.modalUnitIDUDelete.show()
    },
    hideUnitIDUModal() {
      this.flagUnitIDU.delete = false;
      this.modalUnitIDUDelete.hide()
    },
    unitDelete() {
      console.log('Удаление юнита');
      this.fetchDeleteUnitMYP(this.$route.params.id).finally(() => {
        this.flagUnit.delete = false;
        this.modalUnitDelete.hide();
        this.$router.push(`/myp`);
      })
    },
    deleteIDURelation() {
      console.log('Удаление междисциплинарной связи');
      let deleteIDU = { interdisciplinary_id: null }
      this.fetchUpdateUnitMYP(this.$route.params.id, deleteIDU).finally(() => {
        this.unitMYP = { ...this.updatedUnitMYP };
        this.flagUnitIDU.delete = false;
        this.modalUnitIDUDelete.hide();
      })
    }
  },
  mounted() {
    this.modalUnitDelete = new Modal('#modalUnitDelete', { backdrop: 'static' });
    this.modalUnitIDUDelete = new Modal('#modalUnitIDUDelete', { backdrop: 'static' });
    this.fetchGetUnitMYP(this.$route.params.id);
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
}
</script>

<style scoped>
@import '@/assets/css/field.css';
.link {
  cursor: pointer;
  padding: 5px;
}
.link:hover {
  text-decoration: underline;
}
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
.myp-interdisciplinary {
  border: 1px solid #CFCFCF;
  border-radius: 5px;
  padding: 10px;
}
.myp-interdisciplinary:hover {
  background: #CFCFCF;
  transition: 0.5s;
  cursor: pointer;
}
.idu-header {
  text-transform: uppercase;
  font-size: 1.5em;
}
.idu-btn-delete {
  border: none;
  border-radius: 5px;
  padding: 3px 8px;
  font-size: 0.8em;
  margin-top: 5px;
  background: #e44545;
  color: #fff;
  margin-left: auto;
}
.myp-header {
  margin-bottom: 20px;
  margin-top: 10px;
}
.myp-header:not(:first-of-type) {
  margin-top: 20px;
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
  /* flex-basis: 100%; */
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

.post-text {
  flex-basis: 100%;
  font-style: italic;
}

</style>