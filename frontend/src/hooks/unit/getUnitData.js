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

export function getTeachers() {
	const teachers = ref([]);
	const getTeachersData = async () => {
		await axiosAPI.get('/teachers').then((response) => {
			teachers.value = response.data;
		});
	};
	return {
		teachers, getTeachersData
	}
}

export function getGrades() {
	const grades = ref([]);
	const getGradesData = async (program) => {
		const config = {
			params: {
				program: program
			}
		}
		await axiosAPI.get('/grades', config).then((response) => {
			grades.value = response.data;
		});
	};
	return {
		grades, getGradesData
	}
}