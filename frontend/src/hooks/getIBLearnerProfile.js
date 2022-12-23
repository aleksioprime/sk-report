import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getIBLearnerProfile() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const ibProfiles = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getIBLPData = async () => {
		await axios.get(`${BASE_API_URL}/ibprofile`, config).then((response) => {
			ibProfiles.value = response.data;
		});
	};
	onMounted(getIBLPData);
	return {
		ibProfiles
	}
}