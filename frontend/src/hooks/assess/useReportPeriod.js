import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getReportPeriods() {
	const reportPeriods = ref([]);
	const currentReportPeriod = ref({});
	const fetchGetReportPeriods = async (data) => {
		const config = {
			params: {
				study_year: data.study_year || null,
				program: data.program || null,
			}
		}
		await axiosAPI.get('assessment/report/period', config).then((response) => {
			reportPeriods.value = response.data;
			console.log("Получение периодов составления репорта: ", reportPeriods.value)
			currentReportPeriod.value = reportPeriods.value.find((item) => {
				const currentDate = new Date();
				const startDate = new Date(item.date_start);
				const endDate = new Date(item.date_end);
				// console.log(currentDate, startDate, endDate);
				return currentDate > startDate && currentDate < endDate;
			  })
			if (!currentReportPeriod.value) {currentReportPeriod.value = reportPeriods.value.slice(-1)[0]}
			console.log("Текущие период репортов: ", currentReportPeriod.value)
		});
	};
	return {
		reportPeriods, currentReportPeriod, fetchGetReportPeriods
	}
}
