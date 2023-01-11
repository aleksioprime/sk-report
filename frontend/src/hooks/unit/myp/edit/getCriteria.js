import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getCriteria() {
  const criteria = ref([]);
  const url = `${useStore().state.base.baseAPI}/criteria`;
	let config = structuredClone(useStore().state.base.configJWT);
  const getCriteriaData = async (subject) => {
    config.params = {
      subject: subject,
    };
    await axios.get(url, config).then((response) => {
      criteria.value = response.data;
    });
  };
  return {
    criteria, getCriteriaData
  }
}