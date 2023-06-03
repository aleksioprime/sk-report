import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getStudyYears() {
	const studyYears = ref([]);
	const currentStudyYear = ref({
		academic_plan: []
	});
	const fetchGetStudyYears = async () => {
		await axiosAPI.get('/assessment/year').then((response) => {
			studyYears.value = response.data;
			console.log("Получение учебных лет: ", studyYears.value)
			currentStudyYear.value = studyYears.value.find((item) => {
				const currentDate = new Date();
				const startDate = new Date(item.date_start);
				// console.log(new Date(), item.date_start);
				return currentDate > startDate
			  })
			console.log("Текущий год: ", currentStudyYear.value)
		});
	};
	return {
		studyYears, currentStudyYear, fetchGetStudyYears
	}
}
