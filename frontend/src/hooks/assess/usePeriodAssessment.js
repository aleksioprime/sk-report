import { ref, onMounted, computed } from 'vue'
import { axiosAPI } from '@/axios'

export function getAssessmentJournal() {
  const currentPeriod = ref({});
  const currentSubject = ref({ group_ib: {} });
  const currentGroup = ref({ mentor: { user: {} }, class_year: {} });
  const currentClassYear = ref({});
  const fetchGetAssessmentJournal = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        group: data.group || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/journal', config).then((response) => {
      console.log("Загрузка данных для журнала")
      currentPeriod.value = response.data.period;
      currentSubject.value = response.data.subject;
      currentGroup.value = response.data.group;
      currentClassYear.value = response.data.class_year;
      console.log(response.data)
    });
  };
  return {
    currentPeriod, currentSubject, currentGroup, currentClassYear, fetchGetAssessmentJournal
  }
}

export function getAssessmentDnevnik() {
  const marksDnevnik = ref({
    marks: {}
  });
  const isDataDnevnikLoading = ref(true);
  const fetchGetAssessmentDnevnik = async (data) => {
    const config = {
      params: {
        period_dnevnik: data.period_dnevnik || null,
        group_dnevnik: data.group_dnevnik || null,
        subject_dnevnik: data.subject_dnevnik || null,
        user: data.user || null,
      }
    }
    isDataDnevnikLoading.value = false;
    await axiosAPI.get('/assessment/journal/dnevnik', config).then((response) => {
      console.log("Загрузка данных для журнала из Дневника")
      marksDnevnik.value = response.data;
      console.log(response.data)
      isDataDnevnikLoading.value = true;
    });
  };
  return {
    marksDnevnik, isDataDnevnikLoading, fetchGetAssessmentDnevnik
  }
}

export function getSummativeWork() {
  const summativeWorks = ref([]);
  const fetchGetSummativeWork = async (data) => {
    const config = {
      params: {
        teacher: data.teacher || null,
        period: data.period || null,
        group: data.group || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/sumwork', config).then((response) => {
      console.log("Загрузка итоговых работ")
      summativeWorks.value = response.data;
      console.log(summativeWorks.value)
    });
  };
  return {
    summativeWorks, fetchGetSummativeWork
  }
}

export function getStudentsAssessment() {
  const studentsAssessment = ref([]);
  const isStudentsAssessmentLoading = ref(true);
  const fetchGetStudentsAssessment = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        subject: data.subject || null,
      }
    }
    isStudentsAssessmentLoading.value = true;
    await axiosAPI.get('/assessment/student', config).then((response) => {
      studentsAssessment.value = response.data;
      console.log("Студенты: ", studentsAssessment.value)
    }).finally(() => {
      isStudentsAssessmentLoading.value = false;
    });
  };
  return {
    studentsAssessment, isStudentsAssessmentLoading, fetchGetStudentsAssessment
  }
}