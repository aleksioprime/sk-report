import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getAims() {
	const BASE_API_URL = 'http://localhost:8000/api/v1';
	const aims = ref([]);
	// const jwt = this.cookies.get('jwt_token');
	const getAimsData = async (subject) => {
        const config = {
            // headers: {
            //   Authorization: `Bearer ${jwt}`,
            // },
			params: {
			subject: subject,
			},
        };
		await axios.get(`${BASE_API_URL}/aims`, config).then((response) => {
			aims.value = response.data;
		});
	};
	return {
		aims, getAimsData
	}
}