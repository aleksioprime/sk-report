import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getUnits() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const units = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getUnitsData = async () => {
		await axios.get(`${BASE_API_URL}/unitplans/myp`, config).then((response) => {
			units.value = response.data;
		});
	};
	
	onMounted(getUnitsData);
	return {
		units, getUnitsData
	}
}