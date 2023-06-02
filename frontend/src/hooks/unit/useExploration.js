import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getExplorations() {
  const explorations = ref([]);
  const fetchGetExplorations = async (data) => {
    const config = {
      params: {
			  gcontext: data.gcontext || null,
      }
		};
    await axiosAPI.get('myp/explorations', config).then((response) => {
      explorations.value = response.data;
    });
  };
  return {
    explorations, fetchGetExplorations
  }
}
