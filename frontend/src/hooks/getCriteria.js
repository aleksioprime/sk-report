import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getCriteria() {
  const BASE_API_URL = 'http://localhost:8000/api/v1';
  const criteria = ref([]);
  // const jwt = this.cookies.get('jwt_token');
  const getCriteriaData = async (subject) => {
    const config = {
      // headers: {
      //   Authorization: `Bearer ${jwt}`,
      // },
      params: {
        subject: subject,
      },
    };
    await axios.get(`${BASE_API_URL}/criteria`, config).then((response) => {
      criteria.value = response.data;
    });
  };
  return {
    criteria, getCriteriaData
  }
}