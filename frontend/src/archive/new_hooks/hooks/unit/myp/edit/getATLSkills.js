import { ref } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export function getATLSkills() {
	const atlSkills = ref([]);
	const url = `${useStore().state.base.baseAPI}/atlskills`;
	const config = useStore().state.base.configJWT;
	const getATLSkillsData = async () => {
		await axios.get(url, config).then((response) => {
			atlSkills.value = response.data;
		});
	};
	return {
		atlSkills, getATLSkillsData
	}
}