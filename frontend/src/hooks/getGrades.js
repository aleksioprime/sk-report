import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getGrades(program) {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const gradesMYP = ref([]);
	const gradesDP = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getGradesData = async () => {
		await axios.get(`${BASE_API_URL}/grades`, {params: {program: 'MYP'}}).then((response) => {
			gradesMYP.value = response.data;
		});
		await axios.get(`${BASE_API_URL}/grades`, {params: {program: 'DP'}}).then((response) => {
			gradesDP.value = response.data;
		});
	};
	onMounted(getGradesData);
	return {
		gradesMYP, gradesDP
	}
}