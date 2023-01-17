import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getObjectives() {
  const objectives_list = ref([]);
  const url = `${useStore().state.base.baseAPI}/objectives`;
	let config = structuredClone(useStore().state.base.configJWT);
  const getObjectivesData = async (subject, class_year, criteria) => {
    config.params = {
      subject: subject,
      class_year: class_year,
      criteria: criteria,
    };
    await axios.get(url, config).then((response) => {
      objectives_list.value = response.data;
    });
  };
  return {
    objectives_list, getObjectivesData
  }
}