import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getKeyConcepts() {
	const kconcepts = ref([]);
	const url = `${useStore().state.base.baseAPI}/kconcepts`;
	const config = useStore().state.base.configJWT;
	const getKeyConceptsData = async () => {
		await axios.get(url, config).then((response) => {
			kconcepts.value = response.data;
		});
	};
	return {
		kconcepts, getKeyConceptsData
	}
}