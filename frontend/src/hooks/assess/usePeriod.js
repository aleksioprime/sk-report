import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getPeriods() {
	const periods = ref([]);
	const currentPeriod = ref({});
	const fetchGetPeriods = async (data) => {
		const config = {
			params: {
				study_year: data.study_year || null,
				program: data.program || null,
			}
		}
		await axiosAPI.get('/assessment/period', config).then((response) => {
			periods.value = response.data;
			console.log("Получение периодов обучения: ", periods.value)
			currentPeriod.value = periods.value.find((item) => {
				const currentDate = new Date();
				const startDate = new Date(item.date_start);
				const endDate = new Date(item.date_end);
				// console.log(currentDate, startDate, endDate);
				return currentDate > startDate && currentDate < endDate;
			  })
			if (!currentPeriod.value) {currentPeriod.value = periods.value.slice(-1)}
			console.log("Текущие период: ", currentPeriod.value)
		});
	};
	return {
		periods, currentPeriod, fetchGetPeriods
	}
}
