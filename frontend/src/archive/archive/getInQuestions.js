import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getInQuestions() {
	const inquestions = ref([]);
	const url = `${useStore().state.base.baseAPI}/unitplans/myp/inquestion`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getInQuestionsData = async (unit) => {
        config.params = {
			unit: unit,
        };
		await axios.get(url, config).then((response) => {
			inquestions.value = response.data;
		});
	};
	return {
		inquestions, getInQuestionsData
	}
}