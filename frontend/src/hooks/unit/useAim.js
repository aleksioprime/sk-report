import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getAims() {
  const aims = ref([]);
  const fetchGetAims = async (data) => {
    const config = {
      params: {
			  subject: data.subject || null,
        group: data.group || null,
      }
		};
    await axiosAPI.get('myp/aims', config).then((response) => {
      aims.value = response.data;
    });
  };
  return {
    aims, fetchGetAims
  }
}
