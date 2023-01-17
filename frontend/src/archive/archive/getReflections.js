import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getReflections() {
	const reflections = ref([]);
	const url = `${useStore().state.base.baseAPI}/unitplans/myp/reflection`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getReflectionsData = async (unit) => {
        config.params = {
			unit: unit,
        };
		await axios.get(url, config).then((response) => {
			reflections.value = response.data;
		});
	};
	return {
		reflections, getReflectionsData
	}
}