import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

// Запрос на получение информации о текущем периоде, предмете, группе и типах мероприятий 
export function getReportPsychologistJournal() {
  const currentReportPeriod = ref({});
  const currentGroup = ref({ psychologist: { user: {} }, mentor: { user: {} }, class_year: {} });
  const eventTypes = ref([]);  
  const fetchGetReportPsychologist = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        group: data.group || null,
      }
    }
    await axiosAPI.get('/assessment/report/psychologist/journal', config).then((response) => {
      console.log("Загрузка данных для журнала: ", response.data)
      currentReportPeriod.value = response.data.period;
      currentGroup.value = response.data.group;
      eventTypes.value = response.data.event_types;
    });
  };
  return {
    currentReportPeriod, currentGroup, eventTypes, fetchGetReportPsychologist
  }
}


export function getReportsPsychologist() {
  const reportsPsychologist = ref([]);
  const isReportsPsychologistLoading = ref(true);
  const fetchGetReportsPsychologist = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        period: data.period || null,
        class_year: data.class_year || null,
      }
    }
    isReportsPsychologistLoading.value = true;
    await axiosAPI.get('/assessment/student/report/psychologist', config).then((response) => {
      console.log('список студентов с репортами психолога получены: ', response.data)
      reportsPsychologist.value = response.data;
      isReportsPsychologistLoading.value = false;
    });
  };
  return {
    reportsPsychologist, isReportsPsychologistLoading, fetchGetReportsPsychologist
  }
}

export function createReportPsychologist() {
  const createdReportPsychologist = ref([]);
  const fetchCreateReportPsychologist = async (data) => {
    await axiosAPI.post('/assessment/report/psychologist', data).then((response) => {
      console.log('Репорт психолога успешно создан: ', response.data)
      createdReportPsychologist.value = response.data;
    });
  };
  return {
    createdReportPsychologist, fetchCreateReportPsychologist
  }
}

export function updateReportPsychologist() {
  const updatedReportPsychologist = ref([]);
  const fetchUpdateReportPsychologist = async (data) => {
    await axiosAPI.put(`/assessment/report/psychologist/${data.id}`, data).then((response) => {
      console.log('Репорт психолога успешно обновлён: ', response.data)
      updatedReportPsychologist.value = response.data;
    });
  };
  return {
    updatedReportPsychologist, fetchUpdateReportPsychologist
  }
}