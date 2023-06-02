<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/myp">Вернуться к списку юнитов</a></template>
      <template v-slot:header>Работа с юнитпланером MYP</template>
    </base-header>
    <transition name="fade">
    <div v-if="Object.keys(unit).length != 0">
      <h4>
        <div><b>"{{ unit.title }}"</b> ({{ unit.class_year.year_rus }} класс) <small v-if="checkInterdisciplinary" class="badge rounded-pill text-bg-primary">Междисциплинарный юнит</small></div>
        <div v-if="unit.subjects.length || unit.class_year"><span v-for="(sb, index) in unit.subjects" :key="sb.id"><span v-if="index != 0">, </span>{{ sb.subject.name_rus }} ({{ sb.subject.group_ib.name_eng }})</span></div>
      </h4>
      <div class="row mt-4">
        <div class="col-lg-3 border-end">
          <div class="nav nav-pills flex-lg-column mb-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <button class="nav-link" :class="getClassActive(null)"
              id="v-pills-base-tab" data-bs-toggle="pill" data-bs-target="#v-pills-base"
              type="button" role="tab" aria-controls="v-pills-base" aria-selected="true" 
              @click="rememberTab(null)">Основная информация</button>
            <button v-if="checkInterdisciplinary" class="nav-link" id="v-pills-interdisciplinary-tab"
              :class="getClassActive('interdisciplinary')" data-bs-toggle="pill" 
              data-bs-target="#v-pills-interdisciplinary" type="button" role="tab"
              aria-controls="v-pills-interdisciplinary" aria-selected="false" 
              @click="rememberTab('interdisciplinary')">Междисциплинарность</button>
            <button class="nav-link" id="v-pills-inquiry-tab" data-bs-toggle="pill" data-bs-target="#v-pills-inquiry"
              :class="getClassActive('inquiry')" type="button" role="tab" aria-controls="v-pills-inquiry" aria-selected="false"
              @click="rememberTab('inquiry')">Исследование</button>
            <button class="nav-link" id="v-pills-objectives-tab" data-bs-toggle="pill"
              :class="getClassActive('objectives')" data-bs-target="#v-pills-objectives" type="button" role="tab" 
              aria-controls="v-pills-objectives" aria-selected="false" 
              @click="rememberTab('objectives')">Образовательные цели</button>
            <button class="nav-link" id="v-pills-learner-profile-tab" data-bs-toggle="pill"
              :class="getClassActive('profile')" data-bs-target="#v-pills-learner-profile" type="button" role="tab" 
              aria-controls="v-pills-learner-profile" aria-selected="false"
              @click="rememberTab('profile')">Профиль студента</button>
            <button class="nav-link" id="v-pills-assessment-tab" data-bs-toggle="pill"
              :class="getClassActive('assessment')" data-bs-target="#v-pills-assessment" type="button" role="tab" 
              aria-controls="v-pills-assessment" aria-selected="false" 
              @click="rememberTab('assessment')">Оценивание</button>
            <button class="nav-link" id="v-pills-teaching-tab" data-bs-toggle="pill" 
              :class="getClassActive('teaching')" data-bs-target="#v-pills-teaching" type="button" role="tab"
              aria-controls="v-pills-teaching" aria-selected="false" 
              @click="rememberTab('teaching')">Стратегии преподавания</button>
            <button class="nav-link" id="v-pills-reflection-tab" data-bs-toggle="pill"
              :class="getClassActive('reflection')" data-bs-target="#v-pills-reflection" type="button" role="tab"
              aria-controls="v-pills-reflection" aria-selected="false" 
              @click="rememberTab('reflection')">Рефлексия</button>
          </div>
        </div>
        <div class="tab-content w-100 col-md" id="v-pills-tabContent">
          <!-- ОСНОВНАЯ ИНФОРМАЦИЯ -->
          <div class="tab-pane fade" :class="getClassActive(null)" id="v-pills-base" role="tabpanel" aria-labelledby="v-pills-base-tab"
            tabindex="0">
            <!-- Название юнита -->
            <unit-field :fieldName="'title'" :fieldData="unit.title" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit" >
              <template v-slot:read="data">{{ unit[data.field] }}</template>
              <template v-slot:edit="data"><field-text-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Предметы -->
            <unit-field :fieldName="'subjects'" :fieldData="unit.subjects" :fieldEditing="fieldCurrent" :checkLoad="Boolean(subjects_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <div class="d-flex w-100">
                    <div>{{ selectData.field.subject.name_rus }} ({{ selectData.field.subject.group_ib.name_eng.toUpperCase() }}, {{ selectData.field.level.name_eng }})</div>
                    <div></div>
                  </div>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <div class="subjects-adding">
                  <table class="table">
                    <tr v-for="(sb, i) in editUnit[data.field]" :key="i">
                      <td>{{ sb.subject.name_rus }} ({{ sb.subject.group_ib.name_eng }})</td>
                      <td>{{ sb.level.name_eng }}</td>
                      <td>
                        <button class="img-btn-del my-1" @click="deleteSubjectLevel(i)"></button>
                      </td>
                    </tr>
                  </table>
                </div>
                <div class="unit-field-description">Чтобы добавить предмет, выберите его в выпадающем списке и укажите его уровень, а затем нажмите на +</div>
                <div class="row">
                  <div class="col-sm">
                    <select id="level" class="form-select" v-model="choisenSL.subject">
                      <option :value="null">Выберите предмет</option>
                      <option v-for="sb in subjects_list" :key="sb.id" :value="sb">
                        {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
                      </option>
                    </select>
                  </div>
                  <div class="col-sm-4">
                    <select id="level" class="form-select" v-model="choisenSL.level" :disabled="choisenSL.subject == null">
                      <option :value="null">Уровень</option>
                      <option v-for="lv in filteredLevels" :key="lv.id" :value="lv">
                        <div>{{ lv.name_eng }}</div>
                      </option>
                    </select>
                  </div>
                  <div class="col-sm-1 d-flex align-items-center me-2">
                    <button class="img-btn-add" @click="addSubjectLevel" :disabled="choisenSL.subject == null || choisenSL.level == null"></button>
                  </div>
                </div>
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
            <!-- Описание -->
            <unit-field :fieldName="'description'" :fieldData="unit.description" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- МЕЖДИСЦИПЛИНАРНОСТЬ -->
          <div v-if="checkInterdisciplinary" class="tab-pane fade" :class="getClassActive('interdisciplinary')" id="v-pills-interdisciplinary" role="tabpanel"
            aria-labelledby="v-pills-interdisciplinary-tab" tabindex="0">
            <!-- Формы интеграции -->
            <unit-field :fieldName="'form_integration'" :fieldData="unit.inter.form_integration" :fieldEditing="fieldCurrent" 
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"><div v-html="unit.inter[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnitID[data.field]" /></template>
            </unit-field>
            <!-- Цель интеграции -->
            <unit-field :fieldName="'purpose_integration'" :fieldData="unit.inter.purpose_integration" :fieldEditing="fieldCurrent" 
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"><div v-html="unit.inter[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnitID[data.field]" /></template>
            </unit-field>
            <!-- Междисциплинарные связи -->
            <unit-field :fieldName="'interdisciplinary_links'" :fieldData="unit.inter.interdisciplinary_links" :fieldEditing="fieldCurrent" 
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"><div v-html="unit.inter[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnitID[data.field]" /></template>
            </unit-field>
            <!-- Междисциплинарные цели -->
            <unit-field :fieldName="'inter_aims'" :fieldData="unit.inter.inter_aims" :fieldEditing="fieldCurrent" :checkLoad="Boolean(aims_list.length)"
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"> 
                <field-list-view :options="unit.inter[data.field]" v-slot="selectData">
                  <span>{{ firstLetterBig(selectData.field.name_eng) }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnitID[`${data.field}_ids`]" :options="aims_list"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <div>{{ firstLetterBig(selectData.field.name_eng) }}</div>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Междисциплинарные критерии -->
            <unit-field :fieldName="'inter_criteria'" :fieldData="unit.inter.inter_criteria" :fieldEditing="fieldCurrent" :checkLoad="Boolean(criteria_list.length)"
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"> 
                <field-list-view :options="unit.inter[data.field]" v-slot="selectData">
                  <b>{{ selectData.field.letter }}.</b> <span>{{ selectData.field.name_eng }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnitID[`${data.field}_ids`]" :options="criteria_list"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <b>{{ selectData.field.letter }}.</b> <span>{{ selectData.field.name_eng }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Междисциплинарные стрэнды -->
            <unit-field :fieldName="'inter_strands'" :fieldData="unit.inter.inter_strands" :fieldEditing="fieldCurrent" :checkLoad="Boolean(strands_list.length)"
              @edit="editModeID" @save="submitEditID" @cancel="cancelEditID">
              <template v-slot:read="data"> 
                <field-list-view :options="unit.inter[data.field]" v-slot="selectData">
                  <span><b>{{ selectData.field.criterion.letter }}{{ selectData.field.letter }}:</b>
                    {{ firstLetterBig(selectData.field.name_eng) }}</span>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnitID[`${data.field}_ids`]" :options="strands_list"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span><b>{{ selectData.field.criterion.letter }}{{ selectData.field.letter }}:</b>
                    {{ firstLetterBig(selectData.field.name_eng) }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
          </div>
          <!-- ИССЛЕДОВАНИЕ -->
          <div class="tab-pane fade" :class="getClassActive('inquiry')" id="v-pills-inquiry" role="tabpanel" aria-labelledby="v-pills-inquiry-tab"
            tabindex="0">
            <!-- Ключевой концепт -->
            <unit-field :fieldName="'key_concepts'" :fieldData="unit.key_concepts" :fieldEditing="fieldCurrent" :checkLoad="Boolean(key_concepts_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span><b>{{ selectData.field.name_eng }}</b></span>:<br>
                  <div class="ms-3"><small>{{ selectData.field.description_eng }}</small></div>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <div :title="selectData.field.description_eng" :class="{'kc-recomend': checkKeyConcept(selectData.field)}">
                      {{ selectData.field.name_eng }} 
                      (<span v-for="(rs, index) in selectData.field.recommended_subjects" :key="rs.id"><span v-if="index != 0">, </span>{{ rs.name_eng }}</span>)
                    </div>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Сопутствующий концепт -->
            <unit-field :fieldName="'related_concepts'" :fieldData="unit.related_concepts" :fieldEditing="fieldCurrent" :checkLoad="Boolean(related_concepts_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span><b>{{ selectData.field.name_eng }}</b></span>
                  <span v-if="checkInterdisciplinary" >
                    (<span v-for="(rs, index) in selectData.field.subject_directions" :key="rs.id"><span v-if="index != 0">, </span>{{ rs.name_eng }}</span>)
                  </span><br>
                  <div class="ms-3"><small>{{ selectData.field.description_eng }}</small></div>
                </field-list-view>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span data-bs-toggle="tooltip" :title="selectData.field.subject_directions.map(item => item.name_eng).join(', ')">{{ selectData.field.name_eng }}</span> 
                    <!-- <b v-if="checkInterdisciplinary" > 
                      (<span v-for="(rs, index) in selectData.field.subject_directions" :key="rs.id"><span v-if="index != 0">, </span>{{ rs.name_eng }}</span>)
                    </b> -->
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Концептуальное понимание -->
            <unit-field :fieldName="'conceptual_understanding'" :fieldData="unit.conceptual_understanding" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Глобальный контекст -->
            <unit-field :fieldName="'global_context'" :fieldData="unit.global_context" :fieldEditing="fieldCurrent" :checkLoad="Boolean(global_context_list.length)"
               @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
               <template v-slot:read="data">
                  <div><b>{{ unit[data.field].name_eng }}</b>:</div>
                  <div class="ms-3"><small>{{ unit[data.field].description_eng }}</small></div>
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
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit" v-if="unit.global_context">
              <template v-slot:read="data">
                <field-list-view :options="unit[data.field]" v-slot="selectData">
                  <span>- {{ selectData.field.name_eng }}</span>
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
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Исследовательские вопросы -->
            <div>Исследовательские вопросы</div>
            <unit-myp-view-question :unit="unit" @update="getUnitData($route.params.id)" />
          </div>
          <!-- ОБРАЗОВАТЕЛЬНЫЕ ЦЕЛИ -->
          <div class="tab-pane fade" :class="getClassActive('objectives')" id="v-pills-objectives" role="tabpanel" aria-labelledby="v-pills-objectives-tab"
            tabindex="0">
            <!-- Цели -->
            <unit-field :fieldName="'aims'" :fieldData="unit.aims" :fieldEditing="fieldCurrent" :checkLoad="Boolean(aims_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"> 
                <div v-for="(value, field) in groupedField(unit[data.field], 'subject_group')" :key="field">
                  <div v-if="checkInterdisciplinary" class="my-2"><b>{{ subjectGroupUnit.find(item => item.id == field).name_eng }}</b></div>
                  <field-list-view :options="value" v-slot="selectData" class="">
                    <span>- {{ firstLetterBig(selectData.field.name_eng) }}</span>
                  </field-list-view>
                </div>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData" :group="true">
                  <div>
                    <div>{{ firstLetterBig(selectData.field.name_eng) }}</div>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Критерии оценки -->
            <unit-field :fieldName="'criteria'" :fieldData="unit.criteria" :fieldEditing="fieldCurrent" :checkLoad="Boolean(criteria_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <div v-for="(value, field) in groupedField(unit[data.field], 'subject_group')" :key="field">
                  <div v-if="checkInterdisciplinary" class="my-2"><b>{{ subjectGroupUnit.find(item => item.id == field).name_eng }}</b></div>
                  <field-list-view :options="value" v-slot="selectData" class="">
                    <b>{{ selectData.field.letter }}.</b> {{ selectData.field.name_eng }}
                  </field-list-view>
                </div>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData" :group="true">
                  <div><b>{{ selectData.field.letter }}.</b> {{ selectData.field.name_eng }}</div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Стрэнды -->
            <unit-field :fieldName="'strands'" :fieldData="unit.strands" :fieldEditing="fieldCurrent" :checkLoad="Boolean(strands_list.length)"
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data">
                <div v-for="(valueSG, fieldSG) in groupedField(unit[data.field], 'criterion', 'subject_group')" :key="fieldSG">
                  <div v-if="checkInterdisciplinary" class="my-1"><b>{{ getFieldData(subjectGroupUnit, fieldSG).name_eng }}</b></div>
                  <div v-for="(valueCR, fieldCR) in groupedField(valueSG, 'criterion')" :key="fieldCR">
                    <div class="mt-1" ><b>{{ getFieldData(criteriaStrandsUnit, fieldCR).letter }}. {{ getFieldData(criteriaStrandsUnit, fieldCR).name_eng }}</b></div>
                    <field-list-view :options="valueCR" v-slot="selectData" class="ms-3">
                      <span><b>{{ selectData.field.letter }}:</b> {{ firstLetterBig(selectData.field.name_eng) }}</span>
                    </field-list-view>
                  </div>
                </div>
              </template>
              <template v-slot:edit="data">
                <field-checkbox-edit v-model="editUnit[`${data.field}_ids`]" :options="this[`${data.field}_list`]"
                  :fieldName="data.field" v-slot="selectData">
                  <div>
                    <span><b>{{ selectData.field.letter }}:</b>
                    {{ firstLetterBig(selectData.field.name_eng) }}</span>
                  </div>
                </field-checkbox-edit>
              </template>
            </unit-field>
            <!-- Содержание -->
            <unit-field :fieldName="'content'" :fieldData="unit.content" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Умения -->
            <unit-field :fieldName="'skills'" :fieldData="unit.skills" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- ATL-навыки -->
            <div>Карта ATL-навыков</div>
            <unit-myp-view-atl :unit="unit" @update="getUnitData($route.params.id)" />
          </div>
          <!-- ПРОФИЛЬ СТУДЕНТА -->
          <div class="tab-pane fade" :class="getClassActive('profile')" id="v-pills-learner-profile" role="tabpanel"
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
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Межкультурное понимание -->
            <unit-field :fieldName="'international_mindedness'" :fieldData="unit.international_mindedness" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Академическая честность -->
            <unit-field :fieldName="'academic_integrity'" :fieldData="unit.academic_integrity" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Языковое развитие -->
            <unit-field :fieldName="'language_development'" :fieldData="unit.language_development" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Использование средств ИКТ -->
            <unit-field :fieldName="'infocom_technology'" :fieldData="unit.infocom_technology" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Служение как действие -->
            <unit-field :fieldName="'service_as_action'" :fieldData="unit.service_as_action" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- ОЦЕНИВАНИЕ -->
          <div class="tab-pane fade" :class="getClassActive('assessment')" id="v-pills-assessment" role="tabpanel" aria-labelledby="v-pills-assessment-tab"
            tabindex="0">
            <!-- Текущее оценивание -->
            <unit-field :fieldName="'formative_assessment'" :fieldData="unit.formative_assessment" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Итоговое оценивание (задания) -->
            <unit-field :fieldName="'summative_assessment_task'" :fieldData="unit.summative_assessment_task" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Итоговое оценивание (взаимосвязь с исследовательским утверждением) -->
            <unit-field :fieldName="'summative_assessment_soi'" :fieldData="unit.summative_assessment_soi" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Взаимное и самооценивание -->
            <unit-field :fieldName="'peer_self_assessment'" :fieldData="unit.peer_self_assessment" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Стандартизация и модерация -->
            <unit-field :fieldName="'standardization_moderation'" :fieldData="unit.standardization_moderation" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- СТРАТЕГИИ ПРЕПОДАВАНИЯ -->
          <div class="tab-pane fade" :class="getClassActive('teaching')" id="v-pills-teaching" role="tabpanel" aria-labelledby="v-pills-teaching-tab"
            tabindex="0">
            <!-- Предыдущий опыт обучения -->
            <unit-field :fieldName="'prior_experiences'" :fieldData="unit.prior_experiences" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Учебная деятельность -->
            <unit-field :fieldName="'learning_experiences'" :fieldData="unit.learning_experiences" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Стратегии преподавания -->
            <unit-field :fieldName="'teaching_strategies'" :fieldData="unit.teaching_strategies" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Ожидания студентов -->
            <unit-field :fieldName="'student_expectations'" :fieldData="unit.student_expectations" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Обратная связь -->
            <unit-field :fieldName="'feedback'" :fieldData="unit.feedback" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Дифференциация -->
            <unit-field :fieldName="'differentiation'" :fieldData="unit.differentiation" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
            <!-- Ресурсы -->
            <unit-field :fieldName="'resources'" :fieldData="unit.resources" :fieldEditing="fieldCurrent" 
              @edit="editMode" @save="submitEdit" @cancel="cancelEdit">
              <template v-slot:read="data"><div v-html="unit[data.field]"></div></template>
              <template v-slot:edit="data"><field-textarea-edit v-model="editUnit[data.field]" /></template>
            </unit-field>
          </div>
          <!-- РЕФЛЕКСИЯ -->
          <div class="tab-pane fade" :class="getClassActive('reflection')" id="v-pills-reflection" role="tabpanel" aria-labelledby="v-pills-reflection-tab"
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
    </transition>
    <modal-delete :idName="idNameModal" :del="true" @cancel="hideModalDelete" @delete="deleteUnit">
      <div>Вы действитель хотите удалить этот юнит?</div>
    </modal-delete>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
// импорт компонента для работы с исследовательскими вопросами
import UnitMypViewQuestion from "@/components/UnitMYPViewQuestion.vue";
// импорт компонента для работы с картой навыков юнита
import UnitMypViewAtl from "@/components/UnitMYPViewATL.vue";
// импорт компонента для работы с постами рефлексии
import UnitMypViewReflection from "@/components/UnitMYPViewReflection.vue";

import { getSubjectsMYP, getTeachers, getGrades, getLevels } from "@/hooks/unit/getUnitMYPList"
import { getUnitView, getCriteria, getAims,
  getStrands, getKeyConcepts, getRelatedConcepts, 
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
    // Получение функции запроса списка уровней в MYP
    const { levels, getLevelsData } = getLevels();
    // Получение функции запроса списка критериев оценки MYP
    const { criteria_list, getCriteriaData } = getCriteria();
    // Получение функции запроса целей предметных групп
    const { aims_list, getAimsData } = getAims();
    // Получение функции запроса стрендов
    const { strands_list, getStrandsData } = getStrands();
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
    let subjects_list = subjects;
    let authors_list = teachers;
    let class_year_list = grades;
    let level_list = levels;
    return {
      unit, getUnitData, 
      subjects_list, getSubjectsData, 
      authors_list, getTeachersData, 
      class_year_list, getGradesData,
      level_list, getLevelsData,
      criteria_list, getCriteriaData, 
      aims_list, getAimsData, 
      strands_list, getStrandsData, 
      key_concepts_list, getKeyConceptsData,
      related_concepts_list, getRelatedConceptsData, 
      global_context_list, getGlobalContextData, 
      explorations_list, getExplorationsData,
      learner_profile_list, getIBLPData,
    }
  },
  data() {
    return {
      idNameModal: 'Unit',
      editUnit: {},
      choisenSL: { subject: null, level: null },
      editUnitID: {},
      searchAuthors: '',
      fieldCurrent: '',
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
      selectDataFields: ['global_context', 'class_year'],
      multiseelectDataFields: ['criteria', 'learner_profile', 'strands', 'aims', 'explorations', 'key_concepts', 'related_concepts', 'authors', 'inter_aims', 'inter_criteria', 'inter_strands'],
    }
  },
  methods: {
    // Добавление предмета и его уровня в список
    addSubjectLevel() {
      this.editUnit.subjects.push(this.choisenSL);
      this.choisenSL = { subject: null, level: null };
    },
    // Удаление предмета и его уровня из списка
    deleteSubjectLevel(i) {
      this.editUnit.subjects.splice(i, 1); 
    },
    // Показать модальное окно подтверждения удаления юнита
    showModalDelete() {
      this.ModalDelete.show();
    },
    // Скрыть модальное окно подтверждения удаления юнита
    hideModalDelete() {
      this.ModalDelete.hide();
    },
    // Функция удаления текущего юнита
    deleteUnit() {
      this.axios.delete(`/unitplans/myp/${this.$route.params.id}`).then(() => {
        this.ModalDelete.hide();
        this.$router.push('/unit');
      });
    },
    // Функция применения изменений в редактируемом поле юнита
    submitEdit() {
      if (this.editUnit.global_context_id && this.unit.global_context && (this.editUnit.global_context_id !== this.unit.global_context.id)) {
        this.editUnit.explorations_ids = []
      }
      if (this.editUnit.criteria_ids && this.unit.criteria && (this.editUnit.criteria_ids !== this.unit.criteria.map(item => item.id))) {
        this.editUnit.strands_ids = this.unit.strands.filter(item => this.editUnit.criteria_ids.includes(item.criterion.id)).map(item => item.id)
      }
      if (this.editUnit.subjects) {
        const subjectGroups = this.editUnit.subjects.map(item => item.subject.group_ib.id);
        this.editUnit.aims_ids = this.unit.aims.filter(item => subjectGroups.includes(item.subject_group.id)).map(item => item.id);
        this.editUnit.criteria_ids = this.unit.criteria.filter(item => subjectGroups.includes(item.subject_group.id)).map(item => item.id);
        this.editUnit.strands_ids = this.unit.strands.filter(item => subjectGroups.includes(item.criterion.subject_group.id)).map(item => item.id);
        this.editUnit.related_concepts_ids = this.unit.related_concepts.filter(rc => rc.subject_directions.filter( sd => subjectGroups.includes(sd.subject_group.id)).length).map(item => item.id);
        this.editUnit.subjects = [... this.editUnit.subjects.map(item => {  
          return { subject_id: item.subject.id, level_id: item.level.id }
        })]
      }
      this.axios.put(`/unitplans/myp/${this.$route.params.id}`, this.editUnit).then((response) => {
        this.unit = response.data;
        this.editUnit = {};
      });
    },
    // Функция отмены изменений в редактируемом поле юнита
    cancelEdit(field) {
      if (field == 'subjects') {
        this.choisenSL = { subject: null, level: null };
      } else if (this.selectDataFields.includes(field)) {
        delete this.editUnit[`${field}_id`];
      } else if (this.multiseelectDataFields.includes(field)) {
        delete this.editUnit[`${field}_ids`];
      } else {
        delete this.editUnit[field];
      }
    },
    // Активация режима редактирования выбранного поля юнита
    editMode(field) {
      this.fieldCurrent = field;
      // Получение дополнительных данных с сервера при редактировании конкретного поля
      if (field == 'subjects') {
        this.getSubjectsData('ooo', 'base');
        this.getLevelsData();
      } else if (field == 'class_year') {
        this.getGradesData('MYP');
      } else if (field == 'authors') {
        this.getTeachersData();
      } else if (field == 'key_concepts') {
        this.getKeyConceptsData();
      } else if (field == 'related_concepts') {
        this.getRelatedConceptsData(this.unit.subjects.map(item => item.subject.id).toString());
      } else if (field == 'global_context') {
        this.getGlobalContextData();
      } else if (field == 'explorations') {
        this.getExplorationsData(this.unit.global_context.id);
      } else if (field == 'aims') {
        this.getAimsData(this.unit.subjects.map(item => item.subject.id).toString());
      } else if (field == 'criteria') {
        this.getCriteriaData(this.unit.subjects.map(item => item.subject.id).toString());
      } else if (field == 'strands') {
        this.getStrandsData(this.unit.subjects.map(item => item.subject.id).toString(), '', this.unit.criteria.map(item => item.id).toString());
      } else if (field == 'learner_profile') {
        this.getIBLPData();
      }
      // Запись текущих данных во временную переменную редактируемого поля
      if (field == 'subjects') { 
        this.editUnit[field] = [ ...this.unit.subjects ];
      } else if (this.selectDataFields.includes(field)) {
        this.unit[field] ? this.editUnit[`${field}_id`] = this.unit[field].id : this.editUnit[`${field}_id`] = '';
      } else if (this.multiseelectDataFields.includes(field)) {
        this.unit[field] ? this.editUnit[`${field}_ids`] = this.unit[field].map((item) => { return item.id }) : this.editUnit[`${field}_ids`] = [];
      } else {
        this.editUnit[field] = this.unit[field];
      }
    },
    // Функция применения изменений в редактируемом поле МДП
    submitEditID() {
      if (this.editUnitID.inter_criteria_ids && this.unit.inter.inter_criteria && (this.editUnitID.inter_criteria_ids !== this.unit.inter.inter_criteria.map(item => item.id))) {
        this.editUnitID.inter_strands_ids = this.unit.inter.inter_strands.filter(item => this.editUnitID.inter_criteria_ids.includes(item.criterion.id)).map(item => item.id)
      }
      this.axios.put(`/unitplans/myp/inter/${this.unit.inter.id}`, this.editUnitID).then((response) => {
        this.getUnitData(this.$route.params.id);
        this.editUnitID = {};
        console.log('Update UnitID Success');
      });
    },
    // Функция отмены изменений в редактируемом поле МДП
    cancelEditID(field) {
      if (this.selectDataFields.includes(field)) {
        delete this.editUnitID[`${field}_id`];
      } else if (this.multiseelectDataFields.includes(field)) {
        delete this.editUnitID[`${field}_ids`];
      } else {
        delete this.editUnitID[field];
      }
    },
    // Активация режима редактирования выбранного поля МДП
    editModeID(field) {
      this.fieldCurrent = field;
      // Получение дополнительных данных с сервера при редактировании конкретного поля
      if (field == 'inter_aims') {
        this.getAimsData('', 10);
      } else if (field == 'inter_criteria') {
        this.getCriteriaData('', 10);
      } else if (field == 'inter_strands') {
        this.getStrandsData('', 10, this.unit.inter.inter_criteria.map(item => item.id).toString());
      }
      // Запись текущих данных во временную переменную редактируемого поля
      if (this.selectDataFields.includes(field)) {
        this.unit.inter[field] ? this.editUnitID[`${field}_id`] = this.unit.inter[field].id : this.editUnitID[`${field}_id`] = '';
      } else if (this.multiseelectDataFields.includes(field)) {
        this.unit.inter[field] ? this.editUnitID[`${field}_ids`] = this.unit.inter[field].map((item) => { return item.id }) : this.editUnitID[`${field}_ids`] = [];
      } else {
        this.editUnitID[field] = this.unit.inter[field];
      }
    },
    // Проверка ключевого концепта в качестве рекомендованного в предметной группе
    checkKeyConcept(field) {
      return field.recommended_subjects.filter(item => this.unit.subjects.map(item => item.subject.group_ib.id).includes(item.id)).length;
    },
    // Функция делает первую букву заглавной в тексте
    firstLetterBig(text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
    },
    // Группировка списка объектов по выбранному полю
    groupedField(field, name, additionName = '') {
      let groupedObject = field.reduce((acc, obj) => {
        if (additionName) {
          const property = obj[name][additionName].id;
          acc[property] = acc[property] || [];
          acc[property].push(obj);
          return acc;
        } else {
          const property = obj[name].id;
          acc[property] = acc[property] || [];
          acc[property].push(obj);
          return acc;
        }
      }, {});
      return groupedObject;
    },
    getFieldData(value, field) {
      return value.find(item => item.id == field);
    },
    getClassActive(value) {
      return {
        'show active': localStorage.getItem('currentTab') == value
      }
    },
    rememberTab(value) {
      if (value) {
        localStorage.setItem('currentTab', value)
      } else {
        localStorage.removeItem('currentTab');
      }
      
    }
  },
  mounted() {
    this.getUnitData(this.$route.params.id);
    this.ModalDelete = new Modal(`#modalDelete${this.idNameModal}`, { backdrop: 'static' });
  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchAuthors)
    searchTeachers() {
      if (this.searchAuthors == '') {
        return this.authors_list.filter(teacher => this.editUnit.authors_ids.includes(teacher.id))
      }
      return this.authors_list.filter((teacher) => {
        if (teacher.user) {
          return teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.editUnit.authors_ids.includes(teacher.id)
        } else {
          return this.editUnit.authors_ids.includes(teacher.id)
        }
      })
    },
    // Переменная для выборки предменых групп из текущих предметов юнита
    subjectGroupUnit() {
      let objArray = this.unit.subjects.map(sb => sb.subject.group_ib)
      return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    },
    // Переменная для выборки критериев текущих предметов юнита
    criteriaStrandsUnit() {
      let objArray = this.unit.strands.map(item => item.criterion)
      return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    },
    // Переменная с меткой междисциплинарности создаваемого юнита
    checkInterdisciplinary() {
      return this.unit.inter && Object.keys(this.unit.inter).length != 0
    },
    // Переменная с данными отфильтрованных уровней по выбранному предмету
    filteredLevels() {
      let levels = []
      if (this.choisenSL.subject) {
        levels = [...this.level_list.filter(item => item.subject_groups.includes(this.choisenSL.subject.group_ib.id))]
        console.log(levels)
        if (this.unit.class_year.id == 5 || this.unit.class_year.id == 6) {
          this.choisenSL.level = levels[0]
        } else if (this.unit.class_year.id == 7 || this.unit.class_year.id== 8) {
          this.choisenSL.level = levels[1]
        } else {
          this.choisenSL.level = levels[2]
        }
      } 
      return levels
    },
    listDataField(field) {
      // <span v-for="(rs, index) in selectData.field.subject_directions" :key="rs.id"><span v-if="index != 0">, </span>{{ rs.name_eng }}</span>
      return field.subject_directions.map(item => item.name_eng).join(', ')
    }
  },
}
</script>

<style scoped>
@import '@/assets/css/unitview.css';
.text-block {
  white-space: pre-wrap;
}
</style>