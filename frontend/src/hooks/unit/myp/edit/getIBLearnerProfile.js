import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getIBLearnerProfile() {
	const ibProfiles = ref([]);
	const url = `${useStore().state.base.baseAPI}/ibprofile`;
	const config = useStore().state.base.configJWT;
	const getIBLPData = async () => {
		await axios.get(url, config).then((response) => {
			ibProfiles.value = response.data;
		});
	};
	return {
		ibProfiles, getIBLPData
	}
}