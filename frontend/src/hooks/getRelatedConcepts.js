import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getRelatedConcepts() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const rconcepts = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const getRelatedConceptsData = async (subject) => {
		const config = {
			// headers: {
			//   Authorization: `Bearer ${jwt}`,
			// },
			params: {
				subject: subject,
			  },
		};
		await axios.get(`${BASE_API_URL}/rconcepts`, config).then((response) => {
			rconcepts.value = response.data;
		});
	};
	return {
		rconcepts, getRelatedConceptsData
	}
}