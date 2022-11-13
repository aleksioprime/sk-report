import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getGrades(program) {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const grades = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
		params: {
			program: program,
		},
	};
	const getGradesData = async () => {
		await axios.get(`${BASE_API_URL}/grades`, config).then((response) => {
			grades.value = response.data;
		});
	};
	onMounted(getGradesData);
	return {
		grades
	}
}