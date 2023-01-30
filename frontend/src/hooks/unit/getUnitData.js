import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getDepartments() {
	const departments = ref([]);
	const getDepartmentsData = async () => {
		await axiosAPI.get('/departments').then((response) => {
			departments.value = response.data;
		});
	};
	return {
		departments, getDepartmentsData
	}
}