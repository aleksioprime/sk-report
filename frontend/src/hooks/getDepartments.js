import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getDepartments() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const departments = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getDepartmentsData = async () => {
		await axios.get(`${BASE_API_URL}/departments`, config).then((response) => {
			departments.value = response.data;
		});
	};
	onMounted(getDepartmentsData);
	return {
		departments
	}
}