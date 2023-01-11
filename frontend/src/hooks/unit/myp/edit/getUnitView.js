import { ref } from 'vue'
import axios from 'axios';
import { useStore } from 'vuex';

export function getUnitView() {
	const unit = ref([]);
	const url = `${useStore().state.base.baseAPI}/unitplans/myp/`;
	const config = useStore().state.base.configJWT;
	const getUnitData = async (id) => {
		await axios.get(url + id, config).then((response) => {
			unit.value = response.data;
			console.log(unit.value);
		});
	};
	return {
		unit, getUnitData
	}
}