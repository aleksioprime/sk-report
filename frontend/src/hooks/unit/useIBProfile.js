import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getIBProfiles() {
  const ibProfiles = ref([]);
  const fetchGetIBProfiles = async () => {
    await axiosAPI.get('myp/ibprofile').then((response) => {
      ibProfiles.value = response.data;
    });
  };
  return {
    ibProfiles, fetchGetIBProfiles
  }
}
