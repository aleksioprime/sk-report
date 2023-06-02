import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getDepartments() {
  const departments = ref([]);
  const fetchGetDepartments = async () => {
    await axiosAPI.get('departments').then((response) => {
      departments.value = response.data;
    });
  };
  return {
    departments, fetchGetDepartments
  }
}
