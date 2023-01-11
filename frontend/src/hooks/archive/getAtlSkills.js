import { ref, onMounted } from 'vue'
import axios from 'axios';

export function getAtlSkills() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const atlSkills = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const config = {
		// headers: {
		//   Authorization: `Bearer ${jwt}`,
		// },
	};
	const getAtlSkillsData = async () => {
		await axios.get(`${BASE_API_URL}/atlskills`, config).then((response) => {
			atlSkills.value = response.data;
		});
	};
	onMounted(getAtlSkillsData);
	return {
		atlSkills
	}
}