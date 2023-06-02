import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getWorkLoads() {
	const workLoads = ref([]);
	const fetchGetWorkLoads = async (data) => {
        const config = {
			params: {
				teacher: data.teacher || null,
                study_year: data.study_year || null,
			}
		}
		await axiosAPI.get('/workload', config).then((response) => {
			workLoads.value = response.data;
			console.log("Получение нагрузки учителя: ", workLoads.value)
		});
	};
	return {
		workLoads, fetchGetWorkLoads
	}
}

export function createWorkLoad() {
	const createdWorkLoad = ref([]);
	const fetchCreateWorkLoad = async (data) => {
		await axiosAPI.post('/workload', data).then((response) => {
			createdWorkLoad.value = response.data;
			console.log("Создание нагрузки учителя: ", response.data)
		});
	};
	return {
		createdWorkLoad, fetchCreateWorkLoad
	}
}

export function deleteWorkLoad() {
	const fetchDeleteWorkLoad = async (id) => {
		await axiosAPI.delete(`/workload/${id}`).then(() => {
			console.log("Удаление нагрузки учителя")
		});
	};
	return {
		fetchDeleteWorkLoad
	}
}
