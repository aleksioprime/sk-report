<template>
  <div>
    <h1>Работа с юнитом</h1>
    <div class="d-flex">
      <button type="button" class="btn btn-danger ms-auto my-3" @click="showModalUnit()">
        Удалить этот юнит
      </button>
    </div>
    <modal-unit :modalTitle="modalTitle" :del="true" @cancel="hideModalUnit" @delete="deleteUnit">
      <div>Вы действитель хотите удалить этот юнит?</div>
    </modal-unit>
    <div class="d-flex align-items-start mt-3" v-if="Object.keys(unit).length !== 0">
      <div class="nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
        <button class="nav-link active" id="v-pills-base-tab" data-bs-toggle="pill" data-bs-target="#v-pills-base"
          type="button" role="tab" aria-controls="v-pills-base" aria-selected="true">Основная информация</button>
        <button class="nav-link" id="v-pills-inquiry-tab" data-bs-toggle="pill" data-bs-target="#v-pills-inquiry"
          type="button" role="tab" aria-controls="v-pills-inquiry" aria-selected="false">Исследование</button>
        <button class="nav-link" id="v-pills-objectives-tab" data-bs-toggle="pill" data-bs-target="#v-pills-objectives"
          type="button" role="tab" aria-controls="v-pills-objectives" aria-selected="false">Образовательные цели</button>
        <button class="nav-link" id="v-pills-learner-profile-tab" data-bs-toggle="pill" data-bs-target="#v-pills-learner-profile"
          type="button" role="tab" aria-controls="v-pills-learner-profile" aria-selected="false">Профиль студента</button>
        <button class="nav-link" id="v-pills-assessment-tab" data-bs-toggle="pill" data-bs-target="#v-pills-assessment"
          type="button" role="tab" aria-controls="v-pills-assessment" aria-selected="false">Оценивание</button>
        <button class="nav-link" id="v-pills-teaching-tab" data-bs-toggle="pill" data-bs-target="#v-pills-teaching"
          type="button" role="tab" aria-controls="v-pills-teaching" aria-selected="false">Стратегии преподавания</button>
      </div>
      <div class="tab-content w-100" id="v-pills-tabContent">
        <div class="tab-pane fade show active" id="v-pills-base" role="tabpanel" aria-labelledby="v-pills-base-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Название юнита</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.title">
                  <div v-if="unit.title">{{ unit.title }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('title')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description"></div>
                  <input class="form-control unit-field-input" id="title" type="text" v-model="editUnit.title">
                  <button class="unit-field-done" @click="editSaveUnit('title')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('title')">Отмена</button>
                </div>
              </transition>  
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Предмет</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.subject">
                  <div v-if="unit.subject">
                    <span>{{ unit.subject.name_rus }} ({{ unit.subject.group_ib.name_eng }})</span>
                  </div>
                  <div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('subject')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите учебный предмет<br>
                    <span style="color: red;">Внимание: при изменении учебного предмета информация о выбранных критериев оценки, образовательных целях, сопутствующих концептах будет удалена</span></div>
                    <select id="subject" class="form-select" v-model="editUnit.subject_id">
                      <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
                        {{ sb.name_rus }}
                      </option>
                    </select>
                  <button class="unit-field-done" @click="editSaveUnit('subject')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('subject')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Авторы</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.authors">
                  <ul v-if="unit.authors">
                    <li v-for="teacher in unit.authors" :key="teacher.id">
                      {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('authors')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите авторов юнита</div>
                  <div class="flex-grow-1"><input id="authors" class="form-control" type="text" v-model="searchAuthors" placeholder="Введите фамилию для поиска..."></div>
                  <div v-for="teacher in searchTeachers" :key="teacher.id">
                    <div class="form-check">
                      <input class="form-check-input js-authors" type="checkbox" :value="teacher.id" :id="'teacher-' + teacher.id" v-model="editUnit.authors_ids">
                      <label class="form-check-label" :for="'teacher-' + teacher.id">
                        {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('authors')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('authors')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Тип юнита</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.interdisciplinary">
                  <div v-if="unit.interdisciplinary">Междисциплинарный</div>
                  <div v-else>Предметный</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('interdisciplinary')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберит типа юнита</div>
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="radio" name="interdisciplinary" :value="true" id="interdisciplinary-yes" v-model="editUnit.interdisciplinary" disabled>
                      <label class="form-check-label" for="interdisciplinary-yes">
                        <span>Междисциплинарный</span>
                      </label>
                    </div>
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="radio" name="interdisciplinary" :value="false" id="interdisciplinary-no" v-model="editUnit.interdisciplinary">
                      <label class="form-check-label" for="interdisciplinary-no">
                        <span>Предметный</span>
                      </label>
                    </div>
                  <button class="unit-field-done" @click="editSaveUnit('interdisciplinary')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('interdisciplinary')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Год обучения</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.class_year">
                  <div v-if="unit.class_year">
                    <span>{{ unit.class_year.year_ib }} ({{ unit.class_year.year_rus }} класс)</span>
                  </div>
                  <div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('class_year')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите год преподавания юнита в MYP <br>
                    <span style="color: red;">Внимание: при изменении года удаляется информация о выбранных образовательных целях)</span></div>
                    <select id="grades" class="form-select" v-model="editUnit.class_year_id">
                      <option v-for="(gr, i) in grades" :key="i" :value="gr.id">
                        {{ gr.year_rus }} класс ({{ gr.year_ib }})
                      </option>
                    </select>
                  <button class="unit-field-done" @click="editSaveUnit('class_year')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('class_year')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Количество часов</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.hours">
                  <div v-if="unit.hours">{{ unit.hours }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('hours')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description"></div>
                  <input class="form-control unit-field-input" id="hours" type="number" v-model="editUnit.hours">
                  <button class="unit-field-done" @click="editSaveUnit('hours')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('hours')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Описание</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.description">
                  <div v-if="unit.description">{{ unit.description }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('description')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Укажите краткое описание юнита, включая его значение и результат изучения
                  </div>
                  <textarea class="form-control unit-field-input" rows="3" id="description" v-model="editUnit.description"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('description')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('description')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="v-pills-inquiry" role="tabpanel" aria-labelledby="v-pills-inquiry-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Ключевой концепт</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.key_concepts">
                  <ul v-if="unit.key_concepts">
                    <li v-for="kc in unit.key_concepts" :key="kc.id">
                      <span>{{ kc.name_eng }}</span>:<br>
                      <small>{{ kc.description_eng }}</small>
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('key_concepts')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Определите одну ключевую концепцию, которая будет направлять развитие юнита</div>
                  <div v-for="kc in kconcepts" :key="kc.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="checkbox" :value="kc.id" :id="'kconcepts-' + kc.id" v-model="editUnit.key_concepts_ids">
                      <label class="form-check-label" :for="'kconcepts-' + kc.id">
                        <div :class="{'kc-recomend': checkKConcept(kc)}">
                          <span>{{ kc.name_eng }}</span>:<br>
                          <small>{{ kc.description_eng }}</small>
                        </div>
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('key_concepts')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('key_concepts')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Сопутствующий концепт</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.related_concepts">
                  <ul v-if="unit.related_concepts">
                    <li v-for="rc in unit.related_concepts" :key="rc.id">
                      <span>{{ rc.name_eng }}</span>:<br>
                      <small>{{ rc.description_eng }}</small>
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('related_concepts')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Определите одну ключевую концепцию, которая будет направлять развитие юнита</div>
                  <div v-for="rc in rconcepts" :key="rc.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="checkbox" :value="rc.id" :id="'rconcepts-' + rc.id" v-model="editUnit.related_concepts_ids">
                      <label class="form-check-label" :for="'rconcepts-' + rc.id">
                          <span>{{ rc.name_eng }}</span>:<br>
                          <small>{{ rc.description_eng }}</small>
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('related_concepts')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('related_concepts')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Концептуальное понимание</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.conceptual_understanding">
                  <div v-if="unit.conceptual_understanding">{{ unit.conceptual_understanding }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('conceptual_understanding')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Напишите повествовательное предложение, которое отражает взаимосвязь между ключевой концепцией (концепциями) и, если применимо, междисциплинарной предметной концепцией (концепциями)
                  </div>
                  <textarea class="form-control unit-field-input" rows="3" id="conceptual_understanding" v-model="editUnit.conceptual_understanding"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('conceptual_understanding')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('conceptual_understanding')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Глобальный контекст</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.global_context">
                  <div v-if="unit.global_context">
                    <span>{{ unit.global_context.name_eng }}</span>:<br>
                    <small>{{ unit.global_context.description_eng }}</small>
                  </div>
                  <div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('global_context')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите один из шести глобальных контекстов MYP для преподавания и обучения<br>
                    <span style="color: red;">Внимание: при изменении глобального контекста удаляется информация о выбранных линиях исследований)</span></div>
                  <div v-for="gc in gcontext" :key="gc.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="radio" :name="gcontext" :value="gc.id" :id="'gcontext-' + gc.id" v-model="editUnit.global_context_id">
                      <label class="form-check-label" :for="'gcontext-' + gc.id">
                        <span>{{ gc.name_eng }}</span>:<br>
                        <small>{{ gc.description_eng }}</small>
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('global_context')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('global_context')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Линии исследования</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.explorations">
                  <ul v-if="unit.explorations">
                    <li v-for="a in unit.explorations" :key="a.id">
                      {{ a.name_eng  }}
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('explorations')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите, какие предметные цели будут достигнуты в данном юните</div>
                  <div v-for="exp in explorations" :key="exp.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="checkbox" :value="exp.id" :id="'explorations-' + exp.id" v-model="editUnit.explorations_ids">
                      <label class="form-check-label" :for="'explorations-' + exp.id">
                        {{ exp.name_eng }}
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('explorations')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('explorations')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Формулировка исследования</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.statement_inquiry">
                  <div v-if="unit.statement_inquiry">{{ unit.statement_inquiry }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('statement_inquiry')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Сформулируйте утверждение, описывающее концептуальное понимание, которое вы хотите, чтобы студенты запомнили в ходе изучения данного юнита
                  </div>
                  <textarea class="form-control unit-field-input" rows="3" id="statement_inquiry" v-model="editUnit.statement_inquiry"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('statement_inquiry')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('statement_inquiry')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="v-pills-objectives" role="tabpanel" aria-labelledby="v-pills-objectives-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Цели</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.aims">
                  <ul v-if="unit.aims">
                    <li v-for="a in unit.aims" :key="a.id">
                      {{ a.name_eng  }}
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('aims')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите, какие предметные цели будут достигнуты в данном юните</div>
                  <div v-for="a in aims" :key="a.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="checkbox" :value="a.id" :id="'aims-' + a.id" v-model="editUnit.aims_ids">
                      <label class="form-check-label" :for="'aims-' + a.id">
                        {{ a.name_eng }}
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('aims')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('aims')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Образовательные цели</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.objectives">
                  <ul v-if="unit.objectives">
                    <li v-for="obj in unit.objectives" :key="obj.id">
                      <b>{{ obj.strand.criterion.letter  }}{{ obj.strand.letter }}:</b> {{ obj.name_eng }}
                    </li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('objectives')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Какие специальные цели MYP будут решаться в ходе изучения данного юнита?</div>
                  <div v-for="obj in objectives" :key="obj.id">
                    <div class="form-check ms-3">
                      <input class="form-check-input" type="checkbox" :value="obj.id" :id="'objective-' + obj.id" v-model="editUnit.objectives_ids">
                      <label class="form-check-label" :for="'objective-' + obj.id">
                        {{ obj.strand.criterion.letter }}{{ obj.strand.letter }}: {{ obj.name_eng }}
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('objectives')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('objectives')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Содержание (темы, знания и умения)</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.content">
                  <div v-if="unit.content">{{ unit.content }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('content')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Содержание (темы, знания и умения)
                  </div>
                  <textarea class="form-control unit-field-input" rows="10" id="content" v-model="editUnit.content"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('content')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('content')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Умения</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.skills">
                  <div v-if="unit.skills">{{ unit.skills }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('skills')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Какие умения позволят студенту достичь поставленных целей и выполнить задания итоговой работы?
                  </div>
                  <textarea class="form-control unit-field-input" rows="7" id="skills" v-model="editUnit.skills"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('skills')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('skills')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">ATL-умения</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.atl_skills">
                  <ul v-if="unit.atl_skills">
                    <li v-for="atl in unit.atl_skills" :key="atl.id"><b>{{ atl.subcluster.cluster.name_eng }}</b>: {{ atl.name_eng }}</li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('atl_skills')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Выберите умения из группы умений ATL, которые будут отрабатываться в ходе обучения в
                    рамках данного юнита. Вы должны выбрать только те умения, которые Вы явно будете практиковать во время уроков</div>
                  <div v-for="(indicators, cluster) in groupedATL" :key="cluster">
                    <a class="btn" data-bs-toggle="collapse" :href="'#collapse-'+cluster" role="button" aria-expanded="false" :aria-controls="'#collapse-'+cluster">
                      <span :class="{'cluster-atl': checkCluster(cluster)}">{{ findCluster(cluster).name_eng }}</span>
                    </a>
                    <div class="collapse" :id="'collapse-'+cluster">
                      <div v-for="atl in indicators" :key="atl.id" >
                        <div class="form-check ms-3">
                          <input class="form-check-input" type="checkbox" :value="atl.id" :id="'atl-' + atl.id" v-model="editUnit.atl_skills_ids">
                          <label class="form-check-label" :for="'atl-' + atl.id">
                            {{ atl.name_eng }}
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('atl_skills')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('atl_skills')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Развитие ATL-умений</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.description_atl">
                  <div v-if="unit.description_atl">{{ unit.description_atl }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('description_atl')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Для каждого выбранного умения ATL используйте текстовое поле для точного
                    определения:
                    как, где и когда каждый конкретный показатель навыка будет подробно изучаться и практиковаться.
                  </div>
                  <textarea class="form-control unit-field-input" rows="4" id="description_atl" v-model="editUnit.description_atl"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('description_atl')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('description_atl')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="v-pills-learner-profile" role="tabpanel" aria-labelledby="v-pills-learner-profile-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Профили студента</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.learner_profile">
                  <ul v-if="unit.learner_profile">
                    <li v-for="lp in unit.learner_profile" :key="lp.id">{{ lp.name_eng }}</li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('learner_profile')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Какие характеристики профиля студента будут развиваться в ходе изучения юнита?</div>
                  <div v-for="lp in ibProfiles" :key="lp.id">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :value="lp.id" :id="'profile-' + lp.id" v-model="editUnit.learner_profile_ids">
                      <label class="form-check-label" :for="'profile-' + lp.id">
                        {{ lp.name_eng }}: <small>{{ lp.description_eng }}</small>
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('learner_profile')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('learner_profile')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Развитие профиля студента</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.description_learner_profile">
                  <div v-if="unit.description_learner_profile">{{ unit.description_learner_profile }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('description_learner_profile')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как вы будете информировать студентов о развитии качеств профиля студента?</div>
                  <textarea class="form-control unit-field-input" rows="4" id="description_learner_profile" v-model="editUnit.description_learner_profile"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('description_learner_profile')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('description_learner_profile')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Межкультурное понимание</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.international_mindedness">
                  <div v-if="unit.international_mindedness">{{ unit.international_mindedness }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('international_mindedness')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как данный юнит позволит студентам обсудить вопросы глобального значения и / или анализировать проблему с разных культурных точек зрения</div>
                  <textarea class="form-control unit-field-input" rows="4" id="international_mindedness" v-model="editUnit.international_mindedness"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('international_mindedness')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('international_mindedness')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Академическая честность</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.academic_integrity">
                  <div v-if="unit.academic_integrity">{{ unit.academic_integrity }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('academic_integrity')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как принципы академической честности будут реализовываться в ходе изучения данного юнита?</div>
                  <textarea class="form-control unit-field-input" rows="4" id="academic_integrity" v-model="editUnit.academic_integrity"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('academic_integrity')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('academic_integrity')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Языковое развитие</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.language_development">
                  <div v-if="unit.language_development">{{ unit.language_development }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('language_development')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как в ходе изучения данного юнита будет будет поддерживаться языковое развитие студентов</div>
                  <textarea class="form-control unit-field-input" rows="4" id="language_development" v-model="editUnit.language_development"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('language_development')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('language_development')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Использование средств ИКТ</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.infocom_technology">
                  <div v-if="unit.infocom_technology">{{ unit.infocom_technology }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('infocom_technology')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите пути развития информационной грамотности и использования ИКТ в данном юните</div>
                  <textarea class="form-control unit-field-input" rows="4" id="infocom_technology" v-model="editUnit.infocom_technology"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('infocom_technology')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('infocom_technology')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Служение как действие</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.service_as_action">
                  <div v-if="unit.service_as_action">{{ unit.service_as_action }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('service_as_action')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">В какой степени данный юнит вовлекает студентов в принципиальные действия? Что я
                    могу сделать, чтобы использовать данный юнит для развития служения? Какие из следующих результатов обучения
                    поддерживают данный юнит?</div>
                  <textarea class="form-control unit-field-input" rows="4" id="service_as_action" v-model="editUnit.service_as_action"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('service_as_action')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('service_as_action')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="v-pills-assessment" role="tabpanel" aria-labelledby="v-pills-assessment-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Критерии оценки</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.criteria">
                  <ul v-if="unit.criteria">
                    <li v-for="cr in unit.criteria" :key="cr.id">{{ cr.letter }}. {{ cr.name_eng }}</li>
                  </ul>
                  <button class="unit-field-edtbtn" @click="editUnitMode('criteria')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Какие критерии оценивания МУР используются?</div>
                  <div v-for="cr in criteria" :key="cr.id">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="editUnit.criteria_ids">
                      <label class="form-check-label" :for="'criterion-' + cr.id">
                        <b>{{ cr.letter }}.</b> {{ cr.name_eng }}
                      </label>
                    </div>
                  </div>
                  <button class="unit-field-done" @click="editSaveUnit('criteria')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('criteria')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Текущее оценивание</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.formative_assessment">
                  <div v-if="unit.formative_assessment">{{ unit.formative_assessment }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('formative_assessment')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Предоставьте краткое описание итогового (ых) задания (заданий).</div>
                  <textarea class="form-control unit-field-input" rows="4" id="formative_assessment" v-model="editUnit.formative_assessment"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('formative_assessment')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('formative_assessment')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Итоговое оценивание (задания)</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.summative_assessment_task">
                  <div v-if="unit.summative_assessment_task">{{ unit.summative_assessment_task }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('summative_assessment_task')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Предоставьте краткое описание итогового (ых) задания (заданий).</div>
                  <textarea class="form-control unit-field-input" rows="4" id="summative_assessment_task" v-model="editUnit.summative_assessment_task"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('summative_assessment_task')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('summative_assessment_task')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Итоговое оценивание (взаимосвязь с исследовательским утверждением)</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.summative_assessment_soi">
                  <div v-if="unit.summative_assessment_soi">{{ unit.summative_assessment_soi }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('summative_assessment_soi')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Предоставьте краткое описание итогового (ых) задания (заданий).</div>
                  <textarea class="form-control unit-field-input" rows="4" id="summative_assessment_soi" v-model="editUnit.summative_assessment_soi"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('summative_assessment_soi')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('summative_assessment_soi')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Взаимное и самооценивание</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.peer_self_assessment">
                  <div v-if="unit.peer_self_assessment">{{ unit.peer_self_assessment }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('peer_self_assessment')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Напишите возможности, которые будут у студентов для участия во взаимной и самооценке</div>
                  <textarea class="form-control unit-field-input" rows="4" id="peer_self_assessment" v-model="editUnit.peer_self_assessment"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('peer_self_assessment')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('peer_self_assessment')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Стандартизация и модерация</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.standardization_moderation">
                  <div v-if="unit.standardization_moderation">{{ unit.standardization_moderation }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('standardization_moderation')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите процесс стандартизации оценки и процедуры модерации</div>
                  <textarea class="form-control unit-field-input" rows="4" id="standardization_moderation" v-model="editUnit.standardization_moderation"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('standardization_moderation')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('standardization_moderation')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="v-pills-teaching" role="tabpanel" aria-labelledby="v-pills-teaching-tab" tabindex="0">
          <div class="unit-field">
            <div class="unit-field-label">Предыдущий опыт обучения</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.prior_experiences">
                  <div v-if="unit.prior_experiences">{{ unit.prior_experiences }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('prior_experiences')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите предыдущий опыт обучения студентов, связанный с данным юнитом</div>
                  <textarea class="form-control unit-field-input" rows="4" id="prior_experiences" v-model="editUnit.prior_experiences"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('prior_experiences')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('prior_experiences')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Учебная деятельность</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.learning_experiences">
                  <div v-if="unit.learning_experiences">{{ unit.learning_experiences }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('learning_experiences')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Изложите в общих чертах процесс обучения, четко описав, что делают студенты, и напишите этапы, на которых происходит преподавание и усвоение знаний.</div>
                  <textarea class="form-control unit-field-input" rows="4" id="learning_experiences" v-model="editUnit.learning_experiences"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('learning_experiences')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('learning_experiences')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Стратегии преподавания</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.teaching_strategies">
                  <div v-if="unit.teaching_strategies">{{ unit.teaching_strategies }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('teaching_strategies')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Изложите в общих чертах процесс обучения, четко описав, что делают студенты, и напишите этапы, на которых происходит преподавание и усвоение знаний.</div>
                  <textarea class="form-control unit-field-input" rows="4" id="teaching_strategies" v-model="editUnit.teaching_strategies"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('teaching_strategies')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('teaching_strategies')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Ожидания студентов</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.student_expectations">
                  <div v-if="unit.student_expectations">{{ unit.student_expectations }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('student_expectations')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как студенты узнают, что от них ожидается</div>
                  <textarea class="form-control unit-field-input" rows="4" id="student_expectations" v-model="editUnit.student_expectations"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('student_expectations')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('student_expectations')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Обратная связь</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.feedback">
                  <div v-if="unit.feedback">{{ unit.feedback }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('feedback')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите, как обратная связь будет использоваться для поддержки и улучшения обучения студентов во время изучения данного юнита</div>
                  <textarea class="form-control unit-field-input" rows="5" id="feedback" v-model="editUnit.feedback"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('feedback')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('feedback')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
          <div class="unit-field">
            <div class="unit-field-label">Дифференциация</div>
            <div class="unit-field-data">
              <transition name="slide-fade">
                <div v-if="!editMode.differentiation">
                  <div v-if="unit.differentiation">{{ unit.differentiation }}</div><div v-else>Нет данных</div>
                  <button class="unit-field-edtbtn" @click="editUnitMode('differentiation')"></button>
                </div>
                <div v-else>
                  <div class="unit-field-description">Опишите конкретные стратегии, которые будут учитывать разнообразие обучения с точки зрения содержания, процесса и продукта</div>
                  <textarea class="form-control unit-field-input" rows="5" id="differentiation" v-model="editUnit.differentiation"></textarea>
                  <button class="unit-field-done" @click="editSaveUnit('differentiation')">Сохранить</button>
                  <button class="unit-field-cancel" @click="editCancelUnit('differentiation')">Отмена</button>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { getCriteria } from "@/hooks/getCriteria";
import { getObjectives } from "@/hooks/getObjectives";
import { getAims } from "@/hooks/getAims";
import { getIBLearnerProfile } from "@/hooks/getIBLearnerProfile";
import { getAtlSkills } from "@/hooks/getAtlSkills";
import { getGlobalContext } from "@/hooks/getGlobalContext";
import { getExplorations } from "@/hooks/getExplorations";
import { getKeyConcepts } from "@/hooks/getKeyConcepts";
import { getRelatedConcepts } from "@/hooks/getRelatedConcepts";
import { getGrades } from "@/hooks/getGrades";
import { getTeachers } from "@/hooks/getTeachers";
import { getSubjects } from "@/hooks/getSubjects";
import { Modal } from 'bootstrap';

const BASE_API_URL = 'http://localhost:8000/api/v1';

export default {
  name: 'UnitPlansView',
  components: {

  },
  setup(props) {
    const { criteria, getCriteriaData } = getCriteria();
    const { objectives, getObjectivesData } = getObjectives();
    const { aims, getAimsData } = getAims();
    const { explorations, getExplorationsData } = getExplorations();
    const { ibProfiles } = getIBLearnerProfile();
    const { atlSkills } = getAtlSkills();
    const { gcontext } = getGlobalContext();
    const { kconcepts } = getKeyConcepts();
    const { rconcepts, getRelatedConceptsData } = getRelatedConcepts();
    const { grades } = getGrades('MYP');
    const { teachers } = getTeachers();
    const { subjects } = getSubjects('ooo', 'base');
    return {
      criteria, getCriteriaData, ibProfiles, atlSkills, objectives, getObjectivesData, 
      aims, getAimsData, gcontext, explorations, getExplorationsData, kconcepts, rconcepts,
      getRelatedConceptsData, grades, teachers, subjects
    }
  },
  data() {
    return {
      unit: {},
      editMode: {},
      editUnit: {},
      searchAuthors: '',
      modalTitle: '',
    }
  },
  methods: {
    showModalUnit() {
      this.modalTitle = 'Удаление юнита';
      this.modalUnit.show();
    },
    hideModalUnit() {
      this.modalUnit.hide();
    },
    deleteUnit() {
      const config = {
        // headers: {
        //   Authorization: `Bearer ${jwt}`,
        // },
      };
      axios.delete(`${BASE_API_URL}/unitplans/myp/${this.$route.params.id}`, config).then((response) => {
        this.modalUnit.hide();
        this.$router.push('/unitplans');
      });
      
    },
    getUnit(id) {
      const config = {
        // headers: {
        //   Authorization: `Bearer ${jwt}`,
        // },
      };
      axios.get(`${BASE_API_URL}/unitplans/myp/${id}`, config).then((response) => {
        this.unit = response.data;
      });
    },
    updateUnit(requestData, id) {
      const config = {
        // headers: {
        //   Authorization: `Bearer ${jwt}`,
        // },
      };
      if (requestData.global_context_id && (requestData.global_context_id !== this.unit.global_context.id)) {
        requestData.explorations_ids = []
      }
      if (requestData.class_year_id && (requestData.class_year_id !== this.unit.class_year.id)) {
        requestData.objectives_ids = []
      }
      if (requestData.subject_id && (requestData.subject_id !== this.unit.subject.id)) {
        requestData.criteria_ids = []
        requestData.objectives_ids = []
        requestData.related_concepts_ids = []
      }
      axios.put(`${BASE_API_URL}/unitplans/myp/${id}`, requestData, config).then((response) => {
        this.unit = response.data;
      });
    },
    editUnitMode(field) {
      console.log(this.unit);
      const field_ids = ['criteria', 'learner_profile', 'atl_skills', 'objectives', 'aims', 'explorations', 'key_concepts', 'related_concepts', 'authors'];
      const field_id = ['global_context', 'class_year', 'subject'];
      if (field_ids.includes(field)) {
        this.getCriteriaData(this.unit.subject.id);
        this.getObjectivesData(this.unit.subject.id, this.unit.class_year.id, this.unit.criteria.map(item => item.id).toString());
        this.getAimsData(this.unit.subject.id);
        // this.getExplorationsData(this.unit.global_context.id);
        this.getRelatedConceptsData(this.unit.subject.id);
        this.editUnit[`${field}_ids`] = this.unit[field].map((item) => { return item.id });
      } else if (field_id.includes(field)) {
        this.editUnit[`${field}_id`] = this.unit[field].id;
      } else {
        this.editUnit[`${field}`] = this.unit[field];
      }
      this.editMode[field] = true;
    },
    editSaveUnit(field) {
      this.editMode[field] = false;
      // this.unit[field] = this.editUnit[field];
      this.updateUnit(this.editUnit, this.unit.id);
      delete this.editUnit[field];
    },
    editCancelUnit(field) {
      this.editMode[field] = false;
      delete this.editUnit[field];
    },
    findCluster(id) {
      return this.clusters.find(item => item.id == id); 
    },
    checkCluster(id) {
      const filterSkills = this.atlSkills.filter(atl => this.editUnit.atl_skills_ids.includes(atl.id));
      const filterClusters = filterSkills.map((item) => {return item.subcluster.cluster.id});
      return filterClusters.includes(Number(id))
    },
    checkKConcept(kc) {
      const rsubjects = kc.recommended_subjects.map((item) => {return item.id});
      // console.log(rsubjects, this.unit.subject.id, rsubjects.includes(this.unit.subject.id))
      return rsubjects.includes(this.unit.subject.group_ib.id)
    }
  },
  mounted() {
    this.getUnit(this.$route.params.id);
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
  },
  computed: {
    subclusters() {
      const objArray = this.atlSkills.map((atl) => {return atl.subcluster})
      return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    },
    clusters() {
      const objArray = this.subclusters.map((atl) => {return atl.cluster})
      return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    },
    categories() {
      const objArray = this.clusters.map((atl) => {return atl.category})
      return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    },
    groupedATL() {
      let groupedObject = this.atlSkills.reduce((acc, obj) => {
        const property = obj.subcluster.cluster.id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
    searchTeachers () {
      if (this.searchAuthors == '') {
        return this.teachers.filter(teacher => this.editUnit.authors_ids.includes(teacher.id))
      } 
      return this.teachers.filter(teacher => (teacher.user.last_name.toLowerCase().includes(this.searchAuthors.toLowerCase()) || this.editUnit.authors_ids.includes(teacher.id)))
    }
  },
}
</script>

<style scoped>
  .unit-field {
    align-items: center;
    margin-top: 10px;
  }
  .unit-field-data {
    border: 0.5px solid rgb(92, 158, 158);
    padding: 5px;
    width: 100%;
    border-radius: 5px;
    margin-top: 5px;
    font-weight: 500;
    min-height: 40px;
    position: relative;
    white-space: pre-wrap;
    padding-right: 30px;
  }
  .unit-field-data ul {
    margin: 0px;
  }
  .unit-field-edtbtn {
    position: absolute;
    top: 0px;
    right: 5px;
    width: 30px;
    height: 30px;
    border: none;
    background: url('@/assets/img/edit.png') no-repeat 50% 50%;
    background-size: 70%;
    padding: 0;
    margin: 0;
  }
  .unit-field-input {
    margin-top: 5px;
  }
  .unit-field-done, .unit-field-cancel {
    border: none;
    background: rgb(202, 201, 201);
    border-radius: 5px;
    margin: 5px;
    padding: 5px 10px;
  }
  .unit-field-description {
    font-size: 14px;
    margin-bottom: 10px;
  }
  .cluster-atl {
    color: rgb(202, 5, 5);
  }
  .kc-recomend span {
    color: rgb(6, 134, 27);
    text-decoration: underline;
    font-weight: bold;
  }
  /* Анимации появления и исчезновения могут иметь    */
  /* различные продолжительности и функции плавности. */
  .slide-fade-enter-active {
    transition: all 0.2s ease-out;
  }
  .slide-fade-enter-from,
  .slide-fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
  }
</style>