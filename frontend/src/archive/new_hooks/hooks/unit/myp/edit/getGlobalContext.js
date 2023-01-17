import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getGlobalContext() {
	const global_context_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/gcontext`;
	const config = useStore().state.base.configJWT;
	const getGlobalContextData = async () => {
		await axios.get(url, config).then((response) => {
			global_context_list.value = response.data;
		});
	};
	return {
		global_context_list, getGlobalContextData
	}
}