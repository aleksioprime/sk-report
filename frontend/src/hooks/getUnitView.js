import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getUnitView(id) {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const unit = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getUnitData = async () => {
		await axios.get(`${BASE_API_URL}/unitplans/myp/${id}`, config).then((response) => {
			unit.value = response.data;
		});
	};
	
	onMounted(getUnitData);
	return {
		unit, getUnitData
	}
}