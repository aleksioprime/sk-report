import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getAcademicPlan() {
  const academicPlan = ref([]);
  const fetchGetAcademicPlan = async (id) => {
    await axiosAPI.get(`curriculum/academicplans/${id}`).then((response) => {
        console.log('Получен учебный план: ', response.data)
        academicPlan.value = response.data;
    });
  };
  return {
    academicPlan, fetchGetAcademicPlan
  }
}

export function getAcademicPlans() {
  const academicPlans = ref([]);
  const fetchGetAcademicPlans = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
      }
    }
    await axiosAPI.get('curriculum/academicplans', config).then((response) => {
        console.log('Получен список учебных планов: ', response.data)
        academicPlans.value = response.data;
    });
  };
  return {
    academicPlans, fetchGetAcademicPlans
  }
}

export function createHoursSubject() {
  const createdHoursSubject = ref({});
  const fetchCreateHoursSubject = async (data) => {
    await axiosAPI.post(`curriculum/subjecthours`, data).then((response) => {
      console.log('Нагрузка предмета успешно добавлена');
      createdHoursSubject.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    createdHoursSubject, fetchCreateHoursSubject
  }
}


export function updateHoursSubject() {
  const updatedHoursSubject = ref({});
  const fetchUpdateHoursSubject = async (id, data) => {
    await axiosAPI.put(`curriculum/subjecthours/${id}`, data).then((response) => {
      console.log('Нагрузка предмета успешно обновлена');
      updatedHoursSubject.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedHoursSubject, fetchUpdateHoursSubject
  }
}

export function deleteHoursSubject() {
  const fetchDeleteHoursSubject = async (id) => {
    await axiosAPI.delete(`curriculum/subjecthours/${id}`).then(() => {
      console.log('Нагрузка предмета успешно удалена');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return { 
    fetchDeleteHoursSubject
  }
}