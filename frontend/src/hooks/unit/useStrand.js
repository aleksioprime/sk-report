import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getStrands() {
  const strands = ref([]);
  const fetchGetStrands = async (data) => {
    const config = {
      params: {
        criteria: data.criteria || null,
        subject: data.subject || null,
        group: data.group || null,
      }
    }
    await axiosAPI.get('myp/strands', config).then((response) => {
      strands.value = response.data;
    });
  };
  return {
    strands, fetchGetStrands
  }
}
