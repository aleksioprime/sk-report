import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getGlobalContext() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const gcontext = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getGlobalContextData = async () => {
		await axios.get(`${BASE_API_URL}/gcontext`, config).then((response) => {
			gcontext.value = response.data;
		});
	};
	onMounted(getGlobalContextData);
	return {
		gcontext
	}
}