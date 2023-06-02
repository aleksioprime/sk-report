import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getGlobalContext() {
  const globalContexts = ref([]);
  const fetchGetGlobalContexts = async () => {
    await axiosAPI.get('myp/gcontext').then((response) => {
      globalContexts.value = response.data;
    });
  };
  return {
    globalContexts, fetchGetGlobalContexts
  }
}
