import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getLevels() {
  const levels = ref([]);
  const fetchGetLevels = async (data) => {
    const config = {
      params: {
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('myp/levels', config).then((response) => {
      levels.value = response.data;
    });
  };
  return {
    levels, fetchGetLevels
  }
}
