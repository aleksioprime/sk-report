import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getCriteriaMYP() {
  const criteriaMYP = ref([]);
  const fetchGetCriteriaMYP = async (data) => {
    const config = {
      params: {
        subject: data.subject || null,
        group: data.group || null,
      }
    }
    await axiosAPI.get('myp/criteria', config).then((response) => {
      console.log('Получение краткой информации по критериям: ', response.data)
      criteriaMYP.value = response.data;
    });
  };
  return {
    criteriaMYP, fetchGetCriteriaMYP
  }
}

export function getCriteriaDetailMYP() {
  const criteriaMYP = ref([]);
  const fetchGetCriteriaDetailMYP = async (data) => {
    const config = {
      params: {
        subject: data.subject || null,
        group: data.group || null,
      }
    }
    await axiosAPI.get('myp/criteria/detail', config).then((response) => {
      console.log('Получение подробной информации по критериям: ', response.data)
      criteriaMYP.value = response.data;
    });
  };
  return {
    criteriaMYP, fetchGetCriteriaDetailMYP
  }
}