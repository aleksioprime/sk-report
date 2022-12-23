import { ref, onMounted } from 'vue';
import axios from 'axios';

export function getExplorations() {
  const BASE_API_URL = 'http://localhost:8000/api/v1';
  const explorations = ref([]);
  // const jwt = this.cookies.get('jwt_token');
  const getExplorationsData = async (gcontext) => {
    const config = {
      // headers: {
      //   Authorization: `Bearer ${jwt}`,
      // },
      params: {
        gcontext: gcontext,
      },
    };
    await axios.get(`${BASE_API_URL}/explorations`, config).then((response) => {
        explorations.value = response.data;
    });
  };
  return {
    explorations, getExplorationsData
  }
}