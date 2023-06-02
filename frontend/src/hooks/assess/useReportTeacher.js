import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getStudentsReport() {
  const studentsReport = ref([]);
  const isStudentsReportLoading = ref(true);
  const fetchGetStudentsReport = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        subject: data.subject || null,
        study_year: data.study_year || null,
      }
    }
    isStudentsReportLoading.value = true;
    await axiosAPI.get('/assessment/student/report/teacher', config).then((response) => {
      console.log('Получен список студентов для репорта: ', response.data)
      studentsReport.value = response.data;
    }).finally(() => {
      isStudentsReportLoading.value = false;
    });
  };
  return {
    studentsReport, isStudentsReportLoading, fetchGetStudentsReport
  }
}

// Запрос на получение информации о текущем периоде, предмете, группе и типах мероприятий 
export function getReportTeacherJournal() {
  const currentReportPeriod = ref({});
  const currentSubject = ref({ });
  const currentAuthor = ref({ user: {} });
  const currentGroup = ref({ mentor: { user: {} }, class_year: {} });
  const eventTypes = ref([]);  
  const fetchGetReportTeacher = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        group: data.group || null,
        subject: data.subject || null,
        author: data.author || null
      }
    }
    await axiosAPI.get('/assessment/report/teacher/journal', config).then((response) => {
      console.log("Загрузка данных для журнала: ", response.data)
      currentReportPeriod.value = response.data.period;
      currentSubject.value = response.data.subject;
      currentGroup.value = response.data.group;
      eventTypes.value = response.data.event_types;
      if (response.data.author) {
        currentAuthor.value = response.data.author;
      }

    });
  };
  return {
    currentReportPeriod, currentSubject, currentAuthor, currentGroup, eventTypes, fetchGetReportTeacher
  }
}

export function getFinalGradeDnevnik() {
  const gradesDnevnik = ref({
    marks: {}
  });
  const isDataDnevnikLoading = ref(true);
  const fetchGetFinalGradeDnevnik = async (data) => {
    const config = {
      params: {
        period_dnevnik: data.period_dnevnik || null,
        group_dnevnik: data.group_dnevnik || null,
        subject_dnevnik: data.subject_dnevnik || null,
        student_dnevnik: data.student_dnevnik || null,
        user: data.user || null,
      }
    }
    isDataDnevnikLoading.value = false;
    await axiosAPI.get('/assessment/report/teacher/dnevnik', config).then((response) => {
      console.log("Загрузка данных для журнала из Дневника: ", response.data)
      gradesDnevnik.value = response.data;
      isDataDnevnikLoading.value = true;
    });
  };
  return {
    gradesDnevnik, isDataDnevnikLoading, fetchGetFinalGradeDnevnik
  }
}

export function getReportsTeacher() {
  const reportsTeacher = ref([]);
  const isReportsTeacherLoading = ref(true);
  const fetchGetReportsTeacher = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        period: data.period || null,
        subject: data.subject || null,
        class_year: data.class_year || null,
        author: data.author || null,
      }
    }
    isReportsTeacherLoading.value = true;
    await axiosAPI.get('/assessment/report/teacher', config).then((response) => {
      console.log('Репорты получены: ', response.data)
      reportsTeacher.value = response.data;
      isReportsTeacherLoading.value = false;
    });
  };
  return {
    reportsTeacher, isReportsTeacherLoading, fetchGetReportsTeacher
  }
}

export function createReportTeacher() {
  const createdReportTeacher = ref([]);
  const fetchCreateReportTeacher = async (data) => {
    await axiosAPI.post('/assessment/report/teacher', data).then((response) => {
      console.log('Репорт успешно создан: ', response.data)
      createdReportTeacher.value = response.data;
    });
  };
  return {
    createdReportTeacher, fetchCreateReportTeacher
  }
}

export function updateReportTeacher() {
  const updatedReportTeacher = ref([]);
  const fetchUpdateReportTeacher = async (data) => {
    await axiosAPI.put(`/assessment/report/teacher/${data.id}`, data).then((response) => {
      console.log('Репорт успешно обновлён: ', response.data)
      updatedReportTeacher.value = response.data;
    });
  };
  return {
    updatedReportTeacher, fetchUpdateReportTeacher
  }
}