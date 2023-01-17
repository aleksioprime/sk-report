import { ref} from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getGrades() {
	const grades = ref([]);
	const url = `${useStore().state.base.baseAPI}/grades`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getGradesData = async (program) => {
		config.params = {program: program}
		await axios.get(url, config).then((response) => {
			grades.value = response.data;
		});
	};
	return {
		grades, getGradesData
	}
}