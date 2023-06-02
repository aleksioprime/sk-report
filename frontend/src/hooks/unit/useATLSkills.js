import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getATLSkills() {
  const atlSkills = ref([]);
  const fetchGetATLSkills = async () => {
    await axiosAPI.get('myp/atl').then((response) => {
      atlSkills.value = response.data;
    });
  };
  return {
    atlSkills, fetchGetATLSkills
  }
}
