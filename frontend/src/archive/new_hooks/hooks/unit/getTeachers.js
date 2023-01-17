import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getTeachers() {
	const teachers = ref([]);
	const url = `${useStore().state.base.baseAPI}/teachers`;
	const config = useStore().state.base.configJWT;
	const getTeachersData = async () => {
		await axios.get(url, config).then((response) => {
			teachers.value = response.data;
		});
	};
	return {
		teachers, getTeachersData
	}
}