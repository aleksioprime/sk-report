import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getKeyConcepts() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const kconcepts = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getKeyConceptsData = async () => {
		await axios.get(`${BASE_API_URL}/kconcepts`, config).then((response) => {
			kconcepts.value = response.data;
		});
	};
	onMounted(getKeyConceptsData);
	return {
		kconcepts
	}
}