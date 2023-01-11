import {ref, computed} from 'vue'

export function useSortedAndSearchUsers(sortedUsers) {
    const searchQuery = ref('');
    const sortedAndSearchUsers = computed(() => {
        return sortedUsers.value.filter(user => user.last_name.toLowerCase().includes(searchQuery.value.toLowerCase()))
    });
    return {
        searchQuery, sortedAndSearchUsers
    }
};