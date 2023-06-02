import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getObjectives() {
  const objectives = ref([]);
  const fetchGetObjectives = async (data) => {
    const config = {
      params: {
        criterion: data.criterion || null,
        strand: data.strand || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('myp/objectives', config).then((response) => {
      console.log('Получение информации о предметных целях', response.data)
      objectives.value = response.data;
    });
  };
  return {
    objectives, fetchGetObjectives
  }
}
