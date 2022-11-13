import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getSubjects(level, type) {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const subjects = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
    params: {
      level: level,
      type: type,
    },
	};
	const getSubjectsData = async () => {
		await axios.get(`${BASE_API_URL}/subjects`, config).then((response) => {
			subjects.value = response.data;
		});
	};
	onMounted(getSubjectsData);
	return {
		subjects
	}
}