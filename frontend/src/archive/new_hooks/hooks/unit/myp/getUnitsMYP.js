import { ref, onMounted } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getUnitsMYP(queryDepartment) {
	const queryTeacher = ref('')
	const unitsMYP = ref([]);
	const url = `${useStore().state.base.baseAPI}/unitplans/myp`;
	let config = structuredClone(useStore().state.base.configJWT);
	const getUnitsMYPData = async () => {
		config.params = {
			department: queryDepartment.value,
			teacher: queryTeacher.value,
		}
		await axios.get(url, config).then((response) => {
			unitsMYP.value = response.data;
		});
	};
	onMounted(getUnitsMYPData);
	return {
		unitsMYP, queryTeacher, getUnitsMYPData
	}
}