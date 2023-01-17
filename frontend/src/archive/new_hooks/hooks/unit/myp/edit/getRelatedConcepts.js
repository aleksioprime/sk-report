import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getRelatedConcepts() {
	const related_concepts_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/rconcepts`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getRelatedConceptsData = async (subject) => {
		config.params = {
			subject: subject,
		};
		await axios.get(url, config).then((response) => {
			related_concepts_list.value = response.data;
		});
	};
	return {
		related_concepts_list, getRelatedConceptsData
	}
}