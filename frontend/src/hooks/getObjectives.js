import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getObjectives() {
  const BASE_API_URL = 'http://localhost:8000/api/v1';
  const objectives = ref([]);
  // const jwt = this.cookies.get('jwt_token');
  const getObjectivesData = async (subject, class_year, criteria) => {
    const config = {
      // headers: {
      //   Authorization: `Bearer ${jwt}`,
      // },
      params: {
        subject: subject,
        class_year: class_year,
        criteria: criteria,
      },
    };
    await axios.get(`${BASE_API_URL}/objectives`, config).then((response) => {
        objectives.value = response.data;
    });
  };
  return {
    objectives, getObjectivesData
  }
}