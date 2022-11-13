import { ref, onMounted } from 'vue'
import axios from 'axios';

export function useUsers() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const users = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const fetching = async () => {
		await axios.get(`${BASE_API_URL}/user`, config).then((response) => {
			users.value = response.data;
			users.value.forEach((item) => {
				const difData = (new Date().getTime() - new Date(item.date_of_birth));
				item.year = Math.round(difData / (24 * 3600 * 365.25 * 1000));
			});
		});
	};
	onMounted(fetching);
	return {
		users
	}
}