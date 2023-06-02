<template>
  <div>
    <base-header>
      <template v-slot:header>Учебные группы</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <!-- Список групп и студентов в них -->
    <div class="row" v-if="!isGroupLoading">
      <div class="col-sm-4">
        <div v-if="groups.length > 0" ref="grouplist" class="accordion" id="accordionGroups">
          <!-- Список групп -->
          <div v-for="(groupsByYear, year) in groupedArrayData(groups, ['class_year','year_rus'])" :key="year"
            class="accordion-item">
            <h2 class="accordion-header" :id="`heading-${year}`">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                :data-bs-target="`#collapse-${year}`" aria-expanded="false" :aria-controls="`collapse-${year}`">
                {{ year }} классы
              </button>
            </h2>
            <div :id="`collapse-${year}`" class="accordion-collapse collapse" :aria-labelledby="`heading-${year}`"
              data-bs-parent="#accordionGroups">
              <div class="p-1">
                <div v-for="group in groupsByYear" :key="group.id">
                  <group-item :group="group" @select="groupSelect" @update="showUpdateGroup" @delete="showDeleteGroup"
                    :class="[currentGroup && currentGroup.id == group.id ? 'selected' : '']" :showEditButton="currentGroup && currentGroup.id == group.id"/>
                  <div v-if="editingGroupID == group.id" class="m-1">
                    <select id="class_year" class="form-select my-1" v-model="editingGroup.class_year_id">
                      <option v-for="(cy, i) in years" :key="i" :value="cy.id">
                        {{ cy.year_rus }}-й год
                      </option>
                    </select>
                    <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
                    <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
                    <div class="d-flex justify-content-end">
                      <button class="icon icon-confirm mx-1" @click="groupEdit"></button>
                      <button class="icon icon-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                  <div v-else-if="deletingGroupID == group.id" class="m-1">
                    <div>Вы действительно хотите удалить этот класс?</div>
                    <div class="d-flex justify-content-end">
                      <button class="icon icon-confirm mx-1" @click="groupDelete"></button>
                      <button class="icon icon-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                </div>
                <div>
                  <button class="icon icon-add" @click="showAddGroup(year)"></button>
                  <div v-if="addingGroupYear == year" class="m-1">
                    <select id="class_year" class="form-select my-1" v-model="editingGroup.class_year_id">
                      <option v-for="(cy, i) in years" :key="i" :value="cy.id">
                        {{ cy.year_rus }}-й год
                      </option>
                    </select>
                    <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
                    <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
                    <div class="d-flex justify-content-end">
                      <button class="icon icon-confirm mx-1" :disabled="!(editingGroup.class_year && editingGroup.letter)" @click="groupAdd"></button>
                      <button class="icon icon-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button class="btn btn-success btn-sm m-1" @click="showAddGroup()">Создать группу</button>
          <div v-if="addingGroupYear == 0" class="m-1">
            <select id="class_year" class="form-select my-1" v-model="editingGroup.class_year_id">
              <option v-for="(cy, i) in years" :key="i" :value="cy.id">
                {{ cy.year_rus }}-й год
              </option>
            </select>
            <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
            <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
            <div class="d-flex justify-content-end">
              <button class="icon icon-confirm mx-1" :disabled="!(editingGroup.class_year && editingGroup.letter)" @click="groupAdd"></button>
              <button class="icon icon-cancel" @click="groupCancel"></button>
            </div>
          </div>
        </div>
        <div v-else>
          Список групп пуст
        </div>
      </div>
      <div class="col-sm">
        <div v-if="currentGroup">
          <div class="mb-2"><h4>Список студентов <b>{{ currentGroup.class_year }}{{ currentGroup.letter }}</b> класса</h4></div>
          <div class="mb-2">Всего в группе: {{ currentGroup.students.length }} человек</div>
          <div class="mb-2 d-flex align-items-center">
            <div v-if="currentGroup.mentor">Наставник: {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }} {{ currentGroup.mentor.user.last_name }}</div>
            <div v-else>Наставник не выбран</div> 
            <button class="icon icon-edit ms-auto" v-if="!editMentor" @click="showEditMentor"></button>
          </div>
          <div v-if="editMentor" class="border p-2">
            <input id="search-item" class="form-control mb-2" type="text" v-model="queryTeacher" placeholder="Введите текст для поиска...">
            <div v-for="teacher in searchTeachers.slice(0, 5)" :key="teacher.id">
              <div class="form-check ms-3">
                <input class="form-check-input" type="radio" :value="teacher.id" :id="'mentor-' + teacher.id" v-model="editingGroup.mentor_id">
                <label class="form-check-label" :for="'mentor-' + teacher.id">
                  {{ teacher.first_name }} {{ teacher.middle_name }} {{ teacher.last_name }}
                </label>
              </div>
            </div>
            <div class="d-flex mt-2 justify-content-end">
              <button class="btn btn-success" @click="editMentorConfirm" v-if="editingGroup.mentor_id">ОК</button>
              <button class="btn btn-cancel" @click="editMentorCancel">Отмена</button>
            </div>
          </div>
          <div class="mb-2 d-flex align-items-center">
            <div v-if="currentGroup.psychologist">Психолог: {{ currentGroup.psychologist.user.first_name }} {{ currentGroup.psychologist.user.middle_name }} {{ currentGroup.psychologist.user.last_name }}</div>
            <div v-else>Психолог не выбран</div> 
            <button class="icon icon-edit ms-auto" v-if="!editPsycho" @click="showEditPsycho"></button>
          </div>
          <div v-if="editPsycho" class="border p-2">
            <input id="search-item" class="form-control mb-2" type="text" v-model="queryTeacher" placeholder="Введите текст для поиска...">
            <div v-for="teacher in searchTeachers.slice(0, 5)" :key="teacher.id">
              <div class="form-check ms-3">
                <input class="form-check-input" type="radio" :value="teacher.id" :id="'mentor-' + teacher.id" v-model="editingGroup.psychologist_id">
                <label class="form-check-label" :for="'mentor-' + teacher.id">
                  {{ teacher.first_name }} {{ teacher.middle_name }} {{ teacher.last_name }}
                </label>
              </div>
            </div>
            <div class="d-flex mt-2 justify-content-end">
              <button class="btn btn-success" @click="editPsychoConfirm" v-if="editingGroup.psychologist_id">ОК</button>
              <button class="btn btn-cancel" @click="editPsychoCancel">Отмена</button>
            </div>
          </div>
          <div class="border p-2" v-if="currentGroup.students.length">
            <div v-for="(student, index) in currentGroup.students" :key="student.id" class="student-item">
              <div>{{ ++index }}. {{ student.user.last_name }} {{ student.user.first_name }}</div>
              <button class="ms-auto icon icon-del" @click="deleteStudentFromGroup(student)"></button>
            </div>
          </div>
          <div class="border p-2" v-else>В группе нет студентов</div>
          <div class="mt-2">Добавление студентов:</div>
          <div class="d-flex my-2">
            <input class="form-control" type="search" name="search" id="search" placeholder="Введите студента..."
              v-model="searchValue" @keyup.enter="searchStudents" @search="clearStudents">
            <button class="btn btn-primary ms-2" @click="searchStudents" :disabled="!searchValue">Найти</button>
          </div>
          <div v-if="users.length">
            <div class="border student-list">
              <div class="user-item" v-for="user in filterStudentsSearch(users)" :key="user.id">
                <div>{{ user.last_name }} {{ user.first_name }}</div>
                <button class="icon icon-add ms-auto" @click="appendStudentToGroup(user)"></button>
              </div>
            </div>
            <nav aria-label="pagination" class="mt-3 d-flex justify-content-center">
              <ul class="pagination">
                <!-- Ссылка на предыдущую страницу -->
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="prev" @click="changePage(-1)">
                    <span aria-hidden="true">&laquo;</span>
                  </a>
                </li>
                <!-- Ссылка на следующую страницу -->
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="next" @click="changePage(+1)">
                    <span aria-hidden="true">&raquo;</span>
                  </a>
                </li>
              </ul>
            </nav>
          </div>
          <small v-else>
            Для поиска студентов в базе введите фамилию или имя
          </small>
        </div>
        <div v-else class="d-flex justify-content-center align-items-center h-100">Выберите класс</div>
      </div>
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { Collapse } from 'bootstrap';
import GroupItem from "@/components/group/GroupItem";
import { getGroups, retrieveGroup, createGroup, updateGroup, deleteGroup } from "@/hooks/user/useGroup";
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getUsers } from "@/hooks/user/useUser";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getTeachers } from "@/hooks/user/useUser";

export default {
  name: 'GroupBoard',
  components: {
    GroupItem,
  },
  setup(props) {
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { retrievedGroup, fetchRetrieveGroup } = retrieveGroup();
    const { groupedArrayData } = getGroupedArray();
    const { addedGroup, fetchCreateGroup } = createGroup();
    const { updatedGroup, fetchUpdateGroup } = updateGroup();
    const { fetchDeleteGroup } = deleteGroup();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { users, isUserLoading, totalPages, totalUsers, fetchGetUsers } = getUsers();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    const { years, fetchGetClassYears } = getClassYears();
    return {
      groups, isGroupLoading, fetchGetGroups, groupedArrayData,
      retrievedGroup, fetchRetrieveGroup,
      addedGroup, fetchCreateGroup,
      updatedGroup, fetchUpdateGroup,
      fetchDeleteGroup,
      studyYears, currentStudyYear, fetchGetStudyYears,
      users, isUserLoading, totalPages, totalUsers, fetchGetUsers,
      teachers, isTeacherLoading, fetchGetTeachers,
      years, fetchGetClassYears
    }
  },
  data() {
    return {
      currentYear: null,
      currentGroup: null,
      modeAppendStudents: false,
      searchValue: null,
      currentPage: 1,
      limit: 10,
      editingGroupID: null,
      editingGroup: {},
      deletingGroupID: null,
      addingGroupYear: null,
      editMentor: false,
      queryTeacher: null,
      editPsycho: false,
    }
  },
  methods: {
    getAppendStudents() {
      this.modeAppendStudents = true;
    },
    searchStudents() {
      this.fetchGetUsers({ role: "student", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    clearStudents() {
      this.users = [];
    },
    // Выбор текущего пользователя при нажатии на строку списка
    groupSelect(group) {
      if (this.currentGroup != group) {
        this.fetchRetrieveGroup(group).finally(() => {
          this.currentGroup = this.retrievedGroup;
        })
      } else {
        this.currentGroup = null;
      }
    },
    changePage(page) {
      if (this.currentPage > 1 && this.currentPage < this.totalPages) {
        this.currentPage = this.currentPage + page;
      }
      this.fetchGetUsers({ role: "student", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    appendStudentToGroup(user) {
      // this.currentGroup.students.push(user.student);
      this.currentGroup.students_ids = this.currentGroup.students.map(item => item.id)
      this.currentGroup.students_ids.push(user.student.id)
      this.fetchUpdateGroup(this.currentGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup }
      })
    },
    deleteStudentFromGroup(student) {
      this.currentGroup.students = this.currentGroup.students.filter(item => item.id != student.id);
      this.currentGroup.students_ids = this.currentGroup.students.map(item => item.id);
      this.fetchUpdateGroup(this.currentGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup }
      })
    },
    filterStudentsSearch(students) {
      return students.filter(item => !this.currentGroup.students.map(item => item.id).includes(item.student.id))
    },
    showAddGroup(year) {
      if (year) {
        this.addingGroupYear = year;
        this.editingGroup.class_year_id = year;
      } else {
        this.addingGroupYear = 0;
      }
      this.editMentor = false;
    },
    groupAdd() {
      console.log('Запрос на добавление группы: ', this.editingGroup);
      this.fetchCreateGroup(this.editingGroup).finally(() => {
        const currentClassYear = this.editingGroup.class_year_id
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${currentClassYear}`);
          new Collapse(collapse, {toggle: false}).show()
          this.editingGroup = {};
          this.addingGroupYear = null;
          this.currentGroup = null
        });
      })
    },
    showUpdateGroup(group) {
      this.editingGroupID = group.id;
      this.editingGroup = { ...group };
      this.editingGroup.class_year_id = group.class_year.id;
      this.editMentor = false;
    },
    groupEdit() {
      console.log('Запрос на редактирование группы: ', this.editingGroup);
      this.fetchUpdateGroup(this.editingGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup };
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${this.editingGroup.class_year}`);
          new Collapse(collapse, {toggle: false}).show();
          this.editingGroup = {};
          this.editingGroupID = null;
        }); 
      })
    },
    showDeleteGroup(group) {
      this.deletingGroupID = group.id;
      this.editMentor = false;
    },
    groupDelete() {
      console.log('Запрос на удаление группы:', this.deletingGroupID);
      const currentClassYear = this.currentGroup.class_year
      this.currentGroup = null;
      this.fetchDeleteGroup(this.deletingGroupID).finally(() => {
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${currentClassYear}`);
          new Collapse(collapse, {toggle: false}).show()
          this.deletingGroupID = null
        }); 
      })
    },
    groupCancel() {
      this.editingGroup = {};
      this.editingGroupID = null;
      this.deletingGroupID = null;
      this.addingGroupYear = null;
    },
    showEditMentor() {
      this.fetchGetTeachers('mentor');
      this.editingGroup.id = this.currentGroup.id;
      this.queryTeacher = null;
      this.editMentor = true;
    },
    editMentorConfirm() {
      this.editMentor = false;
      console.log('Запрос на редактирование группы: ', this.editingGroup);
      this.fetchUpdateGroup(this.editingGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup };
        this.editingGroup = {};
      })
    },
    editMentorCancel() {
      this.editMentor = false;
      this.editingGroup = {};
    },
    showEditPsycho() {
      this.fetchGetTeachers('mentor');
      this.editingGroup.id = this.currentGroup.id;
      this.queryTeacher = null;
      this.editPsycho = true;
    },
    editPsychoConfirm() {
      this.editPsycho = false;
      console.log('Запрос на редактирование группы: ', this.editingGroup);
      this.fetchUpdateGroup(this.editingGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup };
        this.editingGroup = {};
      })
    },
    editPsychoCancel() {
      this.editPsycho = false;
      this.editingGroup = {};
    }
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.currentYear = this.currentStudyYear;
      this.fetchGetGroups({ study_year: this.currentYear.id });
      this.fetchGetClassYears({});
    });
  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchAuthors)
    searchTeachers() {
      if (!this.queryTeacher) {
        return this.teachers.filter((item, index) => {
          return (index <= 5) || this.editingGroup.mentor_id == item.id
        })
      }
      return this.teachers.filter((item) => {
        if (item.last_name) {
          return item.last_name.toLowerCase().includes(this.queryTeacher.toLowerCase()) || this.editingGroup.mentor_id == item.id
        } else {
          return this.editingGroup.mentor_id == item.id
        }
      })
    }
  },
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';
.student-list {
  display: flex;
  flex-direction: column;
}
.student-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
}
.user-item {
  display: flex;
  align-items: center;
  padding: 10px;
}
</style>