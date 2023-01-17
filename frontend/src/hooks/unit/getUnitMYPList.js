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

export function getUnitsMYP(queryDepartment) {
	const queryTeacher = ref('')
	const unitsMYP = ref([]);
	const getUnitsMYPData = async () => {
		const config = {
			params: {
				department: queryDepartment.value,
				teacher: queryTeacher.value,
			}
		}
		await axiosAPI.get('/unitplans/myp', config).then((response) => {
			unitsMYP.value = response.data;
		});
	};
	return {
		unitsMYP, queryTeacher, getUnitsMYPData
	}
}

export function getSubjectsMYP() {
	const subjects = ref([]);
	const getSubjectsData = async (level, type) => {
		const config = {
			params: {
				level: level,
				type: type,
			}
		}
		await axiosAPI.get('/subjects', config).then((response) => {
			subjects.value = response.data;
		});
	};
	return {
		subjects, getSubjectsData
	}
}

export function getCriteriaMYP() {
  const criteriaMYP = ref([]);
  const getCriteriaData = async () => {
    await axiosAPI.get('/criteria').then((response) => {
      criteriaMYP.value = response.data;
    });
  };
  return {
    criteriaMYP, getCriteriaData
  }
}