<template>
  <div>
    <div v-if="Object.keys(unit).length != 0">
      <base-header>
        <template v-slot:link><a href="/unit">Вернуться к спику юнитов</a></template>
        <template v-slot:header>Работа с юнитпланером MYP</template>
      </base-header>
      <h3>
        <b>"{{ unit.title }}"</b><span class="badge text-bg-primary" v-if="unit.interdisciplinary">Междисциплинарный юнит</span>
        <span v-if="unit.subject || unit.class_year"> - {{ unit.subject.name_rus }} ({{ unit.class_year.year_rus }} класс)</span>
      </h3>
      <div class="row mt-4">
        <div class="col-lg-3 border-end">
          <div class="nav nav-pills flex-lg-column mb-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <button class="nav-link active" id="v-pills-base-tab" data-bs-toggle="pill" data-bs-target="#v-pills-base"
              type="button" role="tab" aria-controls="v-pills-base" aria-selected="true">Основная информация</button>
            <button v-if="unit.interdisciplinary" class="nav-link" id="v-pills-interdisciplinary-tab"
              data-bs-toggle="pill" data-bs-target="#v-pills-interdisciplinary" type="button" role="tab"
              aria-controls="v-pills-interdisciplinary" aria-selected="false">Междисциплинарность</button>
            <button class="nav-link" id="v-pills-inquiry-tab" data-bs-toggle="pill" data-bs-target="#v-pills-inquiry"
              type="button" role="tab" aria-controls="v-pills-inquiry" aria-selected="false">Исследование</button>
            <button class="nav-link" id="v-pills-objectives-tab" data-bs-toggle="pill"
              data-bs-target="#v-pills-objectives" type="button" role="tab" aria-controls="v-pills-objectives"
              aria-selected="false">Образовательные цели</button>
            <button class="nav-link" id="v-pills-learner-profile-tab" data-bs-toggle="pill"
              data-bs-target="#v-pills-learner-profile" type="button" role="tab" aria-controls="v-pills-learner-profile"
              aria-selected="false">Профиль студента</button>
            <button class="nav-link" id="v-pills-assessment-tab" data-bs-toggle="pill"
              data-bs-target="#v-pills-assessment" type="button" role="tab" aria-controls="v-pills-assessment"
              aria-selected="false">Оценивание</button>
            <button class="nav-link" id="v-pills-teaching-tab" data-bs-toggle="pill" data-bs-target="#v-pills-teaching"
              type="button" role="tab" aria-controls="v-pills-teaching" aria-selected="false">Стратегии
              преподавания</button>
            <button class="nav-link" id="v-pills-feedback-tab" data-bs-toggle="pill" data-bs-target="#v-pills-feedback"
              type="button" role="tab" aria-controls="v-pills-feedback" aria-selected="false">Рефлексия</button>
          </div>
        </div>
        
        <div class="tab-content w-100 col-md" id="v-pills-tabContent">
          <!-- ОСНОВНАЯ ИНФОРМАЦИЯ -->
          <div class="tab-pane fade show active" id="v-pills-base" role="tabpanel" aria-labelledby="v-pills-base-tab"
            tabindex="0">
            <!-- Название юнита -->
            <unit-field :fieldName="'title'" :fieldData="unit.title" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit" >
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-text-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Учебный предмет -->
            <unit-field :fieldName="'subject'" :fieldData="unit.subject" :fieldEditing="fieldCurrent" :checkLoad="Boolean(subject_list.length)" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field].name_rus }} ({{ unit[data.field].group_ib.name_eng }})</template>
              <template v-slot:edit="data">
                <field-select-edit v-model="editUnit[`${data.field}_id`]" :options="this[`${data.field}_list`]" v-slot="selectData">
                  <span>{{ selectData.field.name_rus }} ({{ selectData.field.group_ib.name_eng }})</span>
                </field-select-edit>
              </template>
            </unit-field>
            <!-- Авторы юнита -->
            <unit-field :fieldName="'authors'" :fieldData="unit.authors" :fieldEditing="fieldCurrent" :checkLoad="Boolean(authors_list.length)" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="viewData">
                  {{ viewData.field.user.first_name }} {{ viewData.field.user.middle_name }} {{ viewData.field.user.last_name }}
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <input id="search-authors" class="form-control mb-2" type="text" v-model="searchAuthors"
                  placeholder="Введите фамилию для поиска...">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="searchTeachers" :fieldName="data.field"
                  v-slot="selectData">
                  {{ selectData.field.user.first_name }} {{ selectData.field.user.middle_name }} {{
                    selectData.field.user.last_name
                  }}
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Год обучения и часы -->
            <div class="row">
              <div class="col-sm">
                <unit-field :fieldName="'class_year'" :fieldData="unit.class_year" :fieldEditing="fieldCurrent" :checkLoad="Boolean(class_year_list.length)" 
                  @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
                  <template v-slot:read="data">{{ unit[data.field].year_ib }} ({{ unit[data.field].year_rus }} класс)</template>
                  <template v-slot:edit="data">
                    <field-select-edit v-model="editUnit[`${data.field}_id`]" :options="this[`${data.field}_list`]" v-slot="selectData">
                      <span>{{ selectData.field.year_ib }} ({{ selectData.field.year_rus }} класс)</span>
                    </field-select-edit>
                  </template>
                </unit-field>
              </div>
              <div class="col-sm">
                <unit-field :fieldName="'hours'" :fieldData="unit.hours" :fieldEditing="fieldCurrent" 
                  @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
                  <template v-slot:read="data">{{ unit[data.field] }}</template>
                  <template v-slot:edit="data"><field-text-edit v-model="editUnit[data.field]" /></template>
                </unit-field>
              </div>
            </div>
            <!-- Междисциплинарность -->
            <unit-field :fieldName="'interdisciplinary'" :fieldData="unit.interdisciplinary" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit" :txtNoData="'Предметный'">
              <template v-slot:read="data">
                <div v-if="unit[data.field]">Междисциплинарный</div>
                <div v-else>Предметный</div>
              </template>
              <template v-slot:edit="data">
                <field-radio-edit v-model="editUnit[data.field]" :options="interdisciplinary_options"
                  v-slot="selectData">
                  <span>{{ selectData.field.name }}</span>
                </field-radio-edit>
              </template>
            </unit-field>
            <!-- Описание -->
            <unit-field :fieldName="'description'" :fieldData="unit.description" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- МЕЖДИСЦИПЛИНАРНОСТЬ -->
          <div v-if="unit.interdisciplinary" class="tab-pane fade" id="v-pills-interdisciplinary" role="tabpanel"
            aria-labelledby="v-pills-interdisciplinary-tab" tabindex="0">
          </div>
          <!-- ИССЛЕДОВАНИЕ -->
          <div class="tab-pane fade" id="v-pills-inquiry" role="tabpanel" aria-labelledby="v-pills-inquiry-tab"
            tabindex="0">
            <!-- Ключевой концепт -->
            <unit-field :fieldName="'key_concepts'" :fieldData="unit.key_concepts" :fieldEditing="fieldCurrent" :checkLoad="Boolean(key_concepts_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span>:<br>
                  <small>{{ selectData.field.description_eng }}</small>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span>{{ selectData.field.name_eng }}</span>:<br>
                    <small>{{ selectData.field.description_eng }}</small>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Сопутствующий концепт -->
            <unit-field :fieldName="'related_concepts'" :fieldData="unit.related_concepts" :fieldEditing="fieldCurrent" :checkLoad="Boolean(related_concepts_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span><br>
                  <small>{{ selectData.field.description_eng }}</small>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span>{{ selectData.field.name_eng }}</span><br>
                    <small>{{ selectData.field.description_eng }}</small>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Концептуальное понимание -->
            <unit-field :fieldName="'conceptual_understanding'" :fieldData="unit.conceptual_understanding" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Глобальный контекст -->
            <unit-field :fieldName="'global_context'" :fieldData="unit.global_context" :fieldEditing="fieldCurrent" :checkLoad="Boolean(global_context_list.length)"
               @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
               <template v-slot:read="data">
                  <span>{{ unit[data.field].name_eng }}</span>:<br>
                  <small>{{ unit[data.field].description_eng }}</small>
              </template>
              <template v-slot:edit="data">
                <field-radio-edit v-model="editUnit[`${data.field}_id`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span>:<br>
                  <small>{{ selectData.field.description_eng }}</small>
                </field-radio-edit>
              </template>
            </unit-field>
            <!-- Линии исследования -->
            <unit-field :fieldName="'explorations'" :fieldData="unit.explorations" :fieldEditing="fieldCurrent" :checkLoad="Boolean(explorations_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span>{{ selectData.field.name_eng }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Формулировка исследования -->
            <unit-field :fieldName="'statement_inquiry'" :fieldData="unit.statement_inquiry" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <div>Исследовательские вопросы</div>
            <unit-myp-view-question :unit="unit" @update="getUnitData($route.params.id)" />
          </div>
          <!-- ОБРАЗОВАТЕЛЬНЫЕ ЦЕЛИ -->
          <div class="tab-pane fade" id="v-pills-objectives" role="tabpanel" aria-labelledby="v-pills-objectives-tab"
            tabindex="0">
            <!-- Цели -->
            <unit-field :fieldName="'aims'" :fieldData="unit.aims" :fieldEditing="fieldCurrent" :checkLoad="Boolean(aims_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span>{{ selectData.field.name_eng }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Критерии оценки -->
            <unit-field :fieldName="'criteria'" :fieldData="unit.criteria" :fieldEditing="fieldCurrent" :checkLoad="Boolean(criteria_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  {{ selectData.field.letter }}. {{ selectData.field.name_eng }}
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div><b>{{ selectData.field.letter }}.</b> {{ selectData.field.name_eng }}</div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Цели предметной группы -->
            <unit-field :fieldName="'objectives'" :fieldData="unit.objectives" :fieldEditing="fieldCurrent" :checkLoad="Boolean(objectives_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span><b>{{ selectData.field.strand.criterion.letter }}{{ selectData.field.strand.letter }}:</b>
                  {{ selectData.field.name_eng }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span><b>{{ selectData.field.strand.criterion.letter }}{{ selectData.field.strand.letter }}:</b>
                    {{ selectData.field.name_eng }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Содержание -->
            <unit-field :fieldName="'content'" :fieldData="unit.content" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Умения -->
            <unit-field :fieldName="'skills'" :fieldData="unit.skills" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- ATL-навыки -->
            <div>Карта ATL-навыков</div>
            <unit-myp-view-atl :unit="unit" @update="getUnitData($route.params.id)" />
          </div>
          <!-- ПРОФИЛЬ СТУДЕНТА -->
          <div class="tab-pane fade" id="v-pills-learner-profile" role="tabpanel"
            aria-labelledby="v-pills-learner-profile-tab" tabindex="0">
            <!-- Выбор профилей студента для развития -->
            <unit-field :fieldName="'learner_profile'" :fieldData="unit.learner_profile" :fieldEditing="fieldCurrent" :checkLoad="Boolean(learner_profile_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>{{ selectData.field.name_eng }}</span>:<br>
                  <small>{{ selectData.field.description_eng }}</small>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span>{{ selectData.field.name_eng }}</span>:<br>
                    <small>{{ selectData.field.description_eng }}</small>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Описание развития выбранных профилей -->
            <unit-field :fieldName="'description_lp'" :fieldData="unit.description_lp" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Межкультурное понимание -->
            <unit-field :fieldName="'international_mindedness'" :fieldData="unit.international_mindedness" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Академическая честность -->
            <unit-field :fieldName="'academic_integrity'" :fieldData="unit.academic_integrity" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Языковое развитие -->
            <unit-field :fieldName="'language_development'" :fieldData="unit.language_development" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Использование средств ИКТ -->
            <unit-field :fieldName="'infocom_technology'" :fieldData="unit.infocom_technology" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Служение как действие -->
            <unit-field :fieldName="'service_as_action'" :fieldData="unit.service_as_action" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- ОЦЕНИВАНИЕ -->
          <div class="tab-pane fade" id="v-pills-assessment" role="tabpanel" aria-labelledby="v-pills-assessment-tab"
            tabindex="0">
            <!-- Текущее оценивание -->
            <unit-field :fieldName="'formative_assessment'" :fieldData="unit.formative_assessment" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Итоговое оценивание (задания) -->
            <unit-field :fieldName="'summative_assessment_task'" :fieldData="unit.summative_assessment_task" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Итоговое оценивание (взаимосвязь с исследовательским утверждением) -->
            <unit-field :fieldName="'summative_assessment_soi'" :fieldData="unit.summative_assessment_soi" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Взаимное и самооценивание -->
            <unit-field :fieldName="'peer_self_assessment'" :fieldData="unit.peer_self_assessment" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Стандартизация и модерация -->
            <unit-field :fieldName="'standardization_moderation'" :fieldData="unit.standardization_moderation" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- СТРАТЕГИИ ПРЕПОДАВАНИЯ -->
          <div class="tab-pane fade" id="v-pills-teaching" role="tabpanel" aria-labelledby="v-pills-teaching-tab"
            tabindex="0">
            <!-- Предыдущий опыт обучения -->
            <unit-field :fieldName="'prior_experiences'" :fieldData="unit.prior_experiences" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Учебная деятельность -->
            <unit-field :fieldName="'learning_experiences'" :fieldData="unit.learning_experiences" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Стратегии преподавания -->
            <unit-field :fieldName="'teaching_strategies'" :fieldData="unit.teaching_strategies" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Ожидания студентов -->
            <unit-field :fieldName="'student_expectations'" :fieldData="unit.student_expectations" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Обратная связь -->
            <unit-field :fieldName="'feedback'" :fieldData="unit.feedback" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Дифференциация -->
            <unit-field :fieldName="'differentiation'" :fieldData="unit.differentiation" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- РЕФЛЕКСИЯ -->
          <div class="tab-pane fade" id="v-pills-feedback" role="tabpanel" aria-labelledby="v-pills-feedback-tab"
            tabindex="0">
            <unit-myp-view-reflection :unit="unit" :categoryValue="'Prior'" :categoryText="reflectionPriorText" @update="getUnitData($route.params.id)" />
            <unit-myp-view-reflection :unit="unit" :categoryValue="'During'" :categoryText="reflectionDuringText" @update="getUnitData($route.params.id)" />
            <unit-myp-view-reflection :unit="unit" :categoryValue="'After'" :categoryText="reflectionAfterText" @update="getUnitData($route.params.id)" />
          </div>
        </div>
      </div>
      <div class="d-flex border-top mt-3">
        <button type="button" class="btn btn-danger ms-auto my-3" @click="showModalDelete()">
          Удалить этот юнит
        </button>
      </div>
    </div>
    <div v-else>
    </div>
    <modal-delete :idName="idNameModal" :del="true" @cancel="hideModalDelete" @delete="deleteUnit">
      <div>Вы действитель хотите удалить этот юнит?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import axios from 'axios';
import { mapState } from 'vuex'
// импорт компонента для работы с исследовательскими вопросами
import UnitMypViewQuestion from "@/components/UnitMYPViewQuestion.vue";
// импорт компонента для работы с картой навыков юнита
import UnitMypViewAtl from "@/components/UnitMYPViewATL.vue";
// импорт компонента для работы с постами рефлексии
import UnitMypViewReflection from "@/components/UnitMYPViewReflection.vue";

import { getTeachers, getGrades } from "@/hooks/unit/getUnitData"
import { getSubjectsMYP } from "@/hooks/unit/getUnitMYPList"
import { getUnitView, getCriteria, getAims,
  getObjectives, getKeyConcepts, getRelatedConcepts, 
  getGlobalContext, getExplorations, getIBLearnerProfile } from "@/hooks/unit/getUnitMYPEdit"

export default {
  name: 'UnitPlansView',
  components: {
    UnitMypViewQuestion, UnitMypViewAtl, UnitMypViewReflection
  },
  setup(props) {
    // Получение функции запроса данных юнита
    const { unit, getUnitData } = getUnitView();
    // Получение функции запроса списка предметов в MYP
    const { subjects, getSubjectsData } = getSubjectsMYP();
    // Получение функции запроса списка учителей
    const { teachers, getTeachersData } = getTeachers();
    // Получение функции запроса списка годов обучения в MYP
    const { grades, getGradesData } = getGrades();
    // Получение функции запроса списка критериев оценки MYP
    const { criteria_list, getCriteriaData } = getCriteria();
    // Получение функции запроса целей предметных групп
    const { aims_list, getAimsData } = getAims();
    // Получение функции запроса образовательных задач
    const { objectives_list, getObjectivesData } = getObjectives();
    // Получение функции запроса ключевых концептов
    const { key_concepts_list, getKeyConceptsData } = getKeyConcepts();
    // Получение функции запроса связанных концептов
    const { related_concepts_list, getRelatedConceptsData } = getRelatedConcepts();
    // Получение функции запроса глобальных контекстов
    const { global_context_list, getGlobalContextData } = getGlobalContext();
    // Получение функции запроса линий исследования по глобальным контекстам
    const { explorations_list, getExplorationsData } = getExplorations();
    // Получение функции запроса профиля студента
    const { learner_profile_list, getIBLPData } = getIBLearnerProfile();
    // Переименование переменных для полей редактирования
    let subject_list = subjects;
    let authors_list = teachers;
    let class_year_list = grades;
    return {
      unit, getUnitData, subject_list, getSubjectsData, authors_list, getTeachersData, class_year_list, getGradesData,
      criteria_list, getCriteriaData, aims_list, getAimsData, objectives_list, getObjectivesData, key_concepts_list, getKeyConceptsData,
      related_concepts_list, getRelatedConceptsData, global_context_list, getGlobalContextData, explorations_list, getExplorationsData,
      learner_profile_list, getIBLPData
    }
  },
  data() {
    return {
      idNameModal: 'Unit',
      editUnit: {},
      searchAuthors: '',
      fieldCurrent: '',
      interdisciplinary_options: [
        { name: 'Междисциплинарный', id: true },
        { name: 'Предметный', id: false },
      ],
      reflectionPriorText: {
        title: 'До начала изучения',
        description: 'Вопросы, на которых следует сосредоточиться: Почему мы считаем, что юнит или выбор тем будут интересными? Что уже знают студенты и что они могут сделать? Что студенты изучали по данному предмету раньше? Что, по Вашему опыту, можно ожидать в этом юните? Какие качества профиля студента предлагает студентам для развития данный юнит? Какие потенциальные междисциплинарные связи мы можем выявить? Что мы знаем о предпочтениях студентов и моделях взаимодействия? Существуют ли какие-либо возможности для осмысленного изучения направления служение как действие? Что в данном юните может вдохновлять на социальные или персональные проекты? Можем ли мы создать возможности для обучения служению как действию? Как мы можем использовать многоязычие студентов в качестве ресурса для обучения?'
      },
      reflectionDuringText: {
        title: 'В процессе изучения юнита',
        description: 'Вопросы, на которых следует сосредоточиться: С какими трудностями мы столкнулись при изучении юнита или итоговых оценочных заданий? Какие ресурсы оказываются полезными и какие другие ресурсы нам нужны? Какие запросы возникают у студентов? Что мы можем скорректировать или изменить? Какие навыки нуждаются в дополнительной практике? Каков уровень вовлеченности студентов? Как мы можем улучшить обучение студентов, которые нуждаются в поддержке? Что происходит в мире прямо сейчас, с чем мы могли бы связать преподавание и обучение в данном юните? Насколько хорошо учебный опыт согласуется с целями юнита? Какие возможности можно использовать, чтобы помочь студентам получить новые знания, включая личные предпочтения, которые могут быть сохранены, пересмотрены или отвергнуты? (DP теория познания)'
      },
      reflectionAfterText: {
        title: 'По окончании изучения юнита ',
        description: 'Вопросы, на которых следует сосредоточиться: Каковы были результаты обучения в данном юните? Насколько хорошо задание итогового оценивания помогло охарактеризовать уровни достижений? Было ли задание достаточно сложным, чтобы позволить студентам достичь самых высоких уровней? Какие доказательства обучения мы можем выявить? Какие программы обучения мы должны документировать? Какие стратегии обучения были эффективными? Почему? Что было удивительного? Какие действия, инициированные студентами, мы заметили? Что мы сделаем по-другому в следующий раз? Как мы будем использовать наш опыт для планирования следующего юнита? Насколько эффективно мы дифференцировали обучение в данном юните? Что студенты могут вынести из данного юнита на следующий год / уровень обучения? С какими предметными группами мы могли бы поработать в следующий раз? Чему мы научились в результате стандартизации оценки?'
      },
      selectDataFields: ['global_context', 'class_year', 'subject'],
      multiseelectDataFields: ['criteria', 'learner_profile', 'objectives', 'aims', 'explorations', 'key_concepts', 'related_concepts', 'authors'],
    }
  },
  methods: {
    showModalDelete() {
      this.ModalDelete.show();
    },
    hideModalDelete() {
      this.ModalDelete.hide();
    },
    deleteUnit() {
      const url = `${this.api}/unitplans/myp/${this.$route.params.id}`;
      const config = this.configJWT;
      axios.delete(url, config).then(() => {
        this.ModalDelete.hide();
        this.$router.push('/unit');
      });
    },
    // Сохранить изменения в редактируемом поле юнита
    submitEdit() {
      if (this.editUnit.global_context_id && this.unit.global_context && (this.editUnit.global_context_id !== this.unit.global_context.id)) {
        this.editUnit.explorations_ids = []
      }
      if (this.editUnit.criteria_ids && this.unit.criteria && (this.editUnit.criteria_ids !== this.unit.criteria.map(item => item.id))) {
        this.editUnit.objectives_ids = this.unit.objectives.filter(item => this.editUnit.criteria_ids.includes(item.strand.criterion.id)).map(item => item.id)
      }
      if (this.editUnit.subject_id && this.unit.subject &&(this.editUnit.subject_id !== this.unit.subject.id)) {
        this.editUnit.aims_ids = [];
        this.editUnit.criteria_ids = [];
        this.editUnit.objectives_ids = [];
        this.editUnit.related_concepts_ids = [];
      }
      const url = `${this.api}/unitplans/myp/${this.$route.params.id}`;
      const config = this.configJWT;
      axios.put(url, this.editUnit, config).then((response) => {
        this.unit = response.data;
        this.editUnit = {};
        // console.log('Update Unit Success');
      });
    },
    cancelEdit(field) {
      if (this.selectDataFields.includes(field)) {
        delete this.editUnit[`${field}_id`];
      } else if (this.multiseelectDataFields.includes(field)) {
        delete this.editUnit[`${field}_ids`];
      } else {
        delete this.editUnit[field];
      }
    },
    editMode(field) {
      this.fieldCurrent = field;
      if (field == 'subject') {
        this.getSubjectsData('ooo', 'base');
      } else if (field == 'class_year') {
        this.getGradesData('MYP');
      } else if (field == 'authors') {
        this.getTeachersData();
      } else if (field == 'key_concepts') {
        this.getKeyConceptsData();
      } else if (field == 'related_concepts') {
        this.getRelatedConceptsData(this.unit.subject.id);
      } else if (field == 'global_context') {
        this.getGlobalContextData();
      } else if (field == 'explorations') {
        this.getExplorationsData(this.unit.global_context.id);
      } else if (field == 'aims') {
        this.getAimsData(this.unit.subject.id);
      } else if (field == 'criteria') {
        this.getCriteriaData(this.unit.subject.id);
      } else if (field == 'objectives') {
        this.getObjectivesData(this.unit.subject.id, this.unit.class_year.id, this.unit.criteria.map(item => item.id).toString());
      } else if (field == 'learner_profile') {
        this.getIBLPData();
      }
      if (this.selectDataFields.includes(field)) {
        this.unit[field] ? this.editUnit[`${field}_id`] = this.unit[field].id : this.editUnit[`${field}_id`] = '';
      } else if (this.multiseelectDataFields.includes(field)) {
        this.unit[field] ? this.editUnit[`${field}_ids`] = this.unit[field].map((item) => { return item.id }) : this.editUnit[`${field}_ids`] = [];
      } else {
        this.editUnit[field] = this.unit[field];
      }
    },
    // Проверка ключевого концепта в качестве рекомендованного в предметной группе
    checkKC(kc) {
      const rsubjects = kc.recommended_subjects.map((item) => { return item.id });
      return rsubjects.includes(this.unit.subject.group_ib.id)
    }
  },
  mounted() {
    this.getUnitData(this.$route.params.id);
    this.ModalDelete = new Modal(`#modalDelete${this.idNameModal}`, { backdrop: 'static' });
  },
  computed: {
    ...mapState({
      api: state => state.base.baseAPI,
      configJWT: state => state.base.configJWT,
    }),
    searchTeachers() {
      if (this.searchAuthors == '') {
        return this.authors_list.filter(teacher => this.editUnit.authors_ids.includes(teacher.id))
      }
      return this.authors_list.filter(teacher => (teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.editUnit.authors_ids.includes(teacher.id)))
    },
  },
}
</script>

<style scoped>
@import '@/assets/css/unitview.css';
</style>