import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getGlobalContext() {
	const gcontext = ref([]);
	const url = `${useStore().state.base.baseAPI}/gcontext`;
	const config = useStore().state.base.configJWT;
	const getGlobalContextData = async () => {
		await axios.get(url, config).then((response) => {
			gcontext.value = response.data;
		});
	};
	return {
		gcontext, getGlobalContextData
	}
}