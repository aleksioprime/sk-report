import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getGroups() {
  const groups = ref([]);
  const isGroupLoading = ref(false)
  const fetchGetGroups = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
        class_year: data.class_year || null,
        program: data.program || null,
        level: data.level || null,
        teacher: data.teacher || null,
      }
    }
    isGroupLoading.value = true;
    await axiosAPI.get('/assessment/group', config).then((response) => {
      console.log('Список групп успешно получен: ', response.data);
      groups.value = response.data;
    }).finally(() => {
      isGroupLoading.value = false;
    });
  };
  return {
    groups, isGroupLoading, fetchGetGroups
  }
}

export function getGroupsForReportTeacher() {
  const groupsForReportTeacher = ref([]);
  const isGroupLoading = ref(false)
  const fetchGetGroupsForReportTeacher = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
        period: data.period || null,
        level: data.level || null,
        class_year: data.class_year || null,
        teacher: data.teacher || null,
        subject: data.subject || null,
      }
    }
    isGroupLoading.value = true;
    await axiosAPI.get('/report/teacher/groups', config).then((response) => {
      console.log('Список групп для репортов учителей успешно получен: ', response.data);
      groupsForReportTeacher.value = response.data;
    }).finally(() => {
      isGroupLoading.value = false;
    });
  };
  return {
    groupsForReportTeacher, isGroupLoading, fetchGetGroupsForReportTeacher
  }
}

export function getGroupsForReportPsycho() {
  const groupsForReportPsycho = ref([]);
  const isGroupLoading = ref(false)
  const fetchGetGroupsForReportPsycho = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
        period: data.period || null,
        class_year: data.class_year || null,
        psychologist: data.psychologist || null,
      }
    }
    isGroupLoading.value = true;
    await axiosAPI.get('/report/psychologist/groups', config).then((response) => {
      console.log('Список групп для репортов психологов успешно получен: ', response.data);
      groupsForReportPsycho.value = response.data;
    }).finally(() => {
      isGroupLoading.value = false;
    });
  };
  return {
    groupsForReportPsycho, isGroupLoading, fetchGetGroupsForReportPsycho
  }
}

export function getGroupsForReportMentor() {
  const groupsForReportMentor = ref([]);
  const isGroupLoading = ref(false)
  const fetchGetGroupsForReportMentor = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
        period: data.period || null,
        class_year: data.class_year || null,
        mentor: data.mentor || null,
      }
    }
    isGroupLoading.value = true;
    await axiosAPI.get('/report/mentor/groups', config).then((response) => {
      console.log('Список групп для репортов наставников успешно получен: ', response.data);
      groupsForReportMentor.value = response.data;
    }).finally(() => {
      isGroupLoading.value = false;
    });
  };
  return {
    groupsForReportMentor, isGroupLoading, fetchGetGroupsForReportMentor
  }
}

export function getGroupsStudents() {
  const groupsStudents = ref([]);
  const isGroupStudentLoading = ref(false)
  const fetchGetGroupsStudents = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
        class_year: data.class_year || null,
        program: data.program || null,
      }
    }
    isGroupStudentLoading.value = true;
    await axiosAPI.get('/assessment/group/student', config).then((response) => {
      console.log('Список групп со студентами успешно получен: ', response.data);
      groupsStudents.value = response.data;
    }).finally(() => {
      isGroupStudentLoading.value = false;
    });
  };
  return {
    groupsStudents, isGroupStudentLoading, fetchGetGroupsStudents
  }
}

export function retrieveGroup() {
  const retrievedGroup = ref({});
  const fetchRetrieveGroup = async (group) => {
    await axiosAPI.get(`/assessment/group/${group.id}`).then((response) => {
      console.log('Группа успешно получена', response.data);
      retrievedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    retrievedGroup, fetchRetrieveGroup
  }
}

export function createGroup() {
  const addedGroup = ref({});
  const fetchCreateGroup = async (group) => {
    await axiosAPI.post('/assessment/group', group).then((response) => {
      console.log('Группа успешно добавлена');
      addedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    addedGroup, fetchCreateGroup
  }
}

export function updateGroup() {
  const updatedGroup = ref({});
  const fetchUpdateGroup = async (group) => {
    await axiosAPI.put(`/assessment/group/${group.id}`, group).then((response) => {
      console.log('Группа успешно обновлена', response.data);
      updatedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedGroup, fetchUpdateGroup
  }
}

export function deleteGroup() {
  const fetchDeleteGroup = async (group) => {
    await axiosAPI.delete(`/assessment/group/${group}`).then((response) => {
      console.log('Группа успешно удалена');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteGroup
  }
}