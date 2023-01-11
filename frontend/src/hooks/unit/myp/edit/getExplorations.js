import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getExplorations() {
  const explorations = ref([]);
  const url = `${useStore().state.base.baseAPI}/explorations`;
	let config = structuredClone(useStore().state.base.configJWT);
  const getExplorationsData = async (gcontext) => {
    config.params = {
			gcontext: gcontext,
		};
    await axios.get(url, config).then((response) => {
        explorations.value = response.data;
    });
  };
  return {
    explorations, getExplorationsData
  }
}