import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getDepartments() {
	const departments = ref([]);
	const url = `${useStore().state.base.baseAPI}/departments`;
	const config = useStore().state.base.configJWT;
	const getDepartmentsData = async () => {
		await axios.get(url, config).then((response) => {
			departments.value = response.data;
		});
	};
	onMounted(getDepartmentsData);
	return {
		departments
	}
}