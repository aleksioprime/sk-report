import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getATLMapping() {
	const atlmapping = ref([]);
	const url = `${useStore().state.base.baseAPI}/unitplans/myp/atlmapping`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getATLMappingData = async (unit) => {
        config.params = {
			unit: unit,
        };
		await axios.get(url, config).then((response) => {
			atlmapping.value = response.data;
		});
	};
	return {
		atlmapping, getATLMappingData
	}
}