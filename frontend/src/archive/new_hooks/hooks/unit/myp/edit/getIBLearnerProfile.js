import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getIBLearnerProfile() {
	const learner_profile_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/ibprofile`;
	const config = useStore().state.base.configJWT;
	const getIBLPData = async () => {
		await axios.get(url, config).then((response) => {
			learner_profile_list.value = response.data;
		});
	};
	return {
		learner_profile_list, getIBLPData
	}
}