import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getUnitsMYP(queryDepartment) {
	const queryTeacher = ref('');
	const querySubject = ref('');
	const unitsMYP = ref([]);
	const getUnitsMYPData = async () => {
		const config = {
			params: {
				department: queryDepartment.value,
				teacher: queryTeacher.value,
				subject: querySubject.value,
			}
		}
		await axiosAPI.get('/unitplans/myp', config).then((response) => {
			unitsMYP.value = response.data;
		});
	};
	return {
		unitsMYP, queryTeacher, querySubject, getUnitsMYPData
	}
}

export function getTeachers() {
	const teachers = ref([]);
	const getTeachersData = async () => {
		await axiosAPI.get('/teachers').then((response) => {
			teachers.value = response.data;
			// console.log(teachers.value)
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

export function getLevels() {
	const levels = ref([]);
	const getLevelsData = async () => {
	  await axiosAPI.get('/levels').then((response) => {
		levels.value = response.data;
	  });
	};
	return {
	  levels, getLevelsData
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
