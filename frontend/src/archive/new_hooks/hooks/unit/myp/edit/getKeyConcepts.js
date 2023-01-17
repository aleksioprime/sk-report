import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getKeyConcepts() {
	const key_concepts_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/kconcepts`;
	const config = useStore().state.base.configJWT;
	const getKeyConceptsData = async () => {
		await axios.get(url, config).then((response) => {
			key_concepts_list.value = response.data;
		});
	};
	return {
		key_concepts_list, getKeyConceptsData
	}
}