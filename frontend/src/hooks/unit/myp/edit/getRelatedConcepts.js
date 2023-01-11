import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getRelatedConcepts() {
	const rconcepts = ref([]);
	const url = `${useStore().state.base.baseAPI}/rconcepts`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getRelatedConceptsData = async (subject) => {
		config.params = {
			subject: subject,
		};
		await axios.get(url, config).then((response) => {
			rconcepts.value = response.data;
		});
	};
	return {
		rconcepts, getRelatedConceptsData
	}
}