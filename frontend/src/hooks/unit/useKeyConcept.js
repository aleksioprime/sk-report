import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getKeyConcepts() {
  const keyConcepts = ref([]);
  const fetchGetKeyConcepts = async () => {
    await axiosAPI.get('myp/kconcepts').then((response) => {
      keyConcepts.value = response.data;
    });
  };
  return {
    keyConcepts, fetchGetKeyConcepts
  }
}
