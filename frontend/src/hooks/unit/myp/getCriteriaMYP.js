import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getCriteriaMYP() {
  const criteriaMYP = ref([]);
  const url = `${useStore().state.base.baseAPI}/criteria`;
	const config = useStore().state.base.configJWT;
  const getCriteriaData = async () => {
    await axios.get(url, config).then((response) => {
      criteriaMYP.value = response.data;
    });
    
  };
  return {
    criteriaMYP, getCriteriaData
  }
}