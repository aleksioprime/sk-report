import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getUsers() {
	const users = ref([]);
	const getUserData = async (role) => {
		const config = {
			params: {
				role: role,
			}
		}
		await axiosAPI.get('/user', config).then((response) => {
			users.value = response.data;
			users.value.forEach((item) => {
				const difData = (new Date().getTime() - new Date(item.date_of_birth));
				item.year = Math.round(difData / (24 * 3600 * 365.25 * 1000));
			});
		});
	};
	return {
		users, getUserData
	}
}

export function getRoles() {
	const roles = ref([]);
	const getRolesData= async () => {
		await axiosAPI.get('/role').then((response) => {
			roles.value = response.data;
		});
	};
	return {
		roles, getRolesData
	}
}

export function getGroups() {
	const groups = ref([]);
	const getGroupsData= async () => {
		await axiosAPI.get('/class').then((response) => {
			groups.value = response.data;
		});
	};
	return {
		groups, getGroupsData
	}
}