import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getSubjectsMYP() {
	const subjects = ref([]);
	const url = `${useStore().state.base.baseAPI}/subjects`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getSubjectsData = async (level, type) => {
		config.params = {
			level: level,
			type: type,
		}
		await axios.get(url, config).then((response) => {
			subjects.value = response.data;
		});
	};
	// onMounted(getSubjectsData);
	return {
		subjects, getSubjectsData
	}
}