import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getWorkGroup() {
	const workGroup = ref({
		work: {
			criteria: []
		},
		students: []
	});
	const getWorkGroupData = async (id) => {
		await axiosAPI.get(`/assessment/workgroup/${id}`).then((response) => {
			console.log("Загрузка итоговой работы")
			workGroup.value = response.data;
			console.log(workGroup.value)
		});
	};
	return {
		workGroup, getWorkGroupData
	}
}

export function getStudents() {
	const students = ref([]);
	const getStudentsData = async (data) => {
		const config = {
			params: {
				class: data.class || null,
			}
		}
		await axiosAPI.get('/student', config).then((response) => {
			students.value = response.data;
			console.log("Студенты: ", students.value)
		});
	};
	return {
		students, getStudentsData
	}
}

export function getWorkAssess() {
	const workAssess = ref([]);
	const getWorkAssessData = async (group, callback) => {
    const config = {
			params: {
				class: group,
			}
		}
		await axiosAPI.get(`/assessment/workassess`, config).then((response) => {
			console.log("Загрузка оценок за итоговые работы")
			workAssess.value = response.data;
			console.log(workAssess.value)
			callback();
		});
	};
	return {
		workAssess, getWorkAssessData
	}
}