import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getTeachers() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const teachers = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getTeachersData = async () => {
		await axios.get(`${BASE_API_URL}/teachers`, config).then((response) => {
			teachers.value = response.data;
		});
	};
	onMounted(getTeachersData);
	return {
		teachers
	}
}