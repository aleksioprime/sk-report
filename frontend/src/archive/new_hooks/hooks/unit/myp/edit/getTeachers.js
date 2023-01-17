import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getTeachers() {
	const authors_list = ref([]);
	const url = `${useStore().state.base.baseAPI}/teachers`;
	const config = useStore().state.base.configJWT;
	const getTeachersData = async () => {
		await axios.get(url, config).then((response) => {
			authors_list.value = response.data;
		});
	};
	return {
		authors_list, getTeachersData
	}
}