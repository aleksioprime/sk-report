import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getAims() {
	const aims_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/aims`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getAimsData = async (subject) => {
        config.params = {
			subject: subject,
        };
		await axios.get(url, config).then((response) => {
			aims_list.value = response.data;
		});
	};
	return {
		aims_list, getAimsData
	}
}