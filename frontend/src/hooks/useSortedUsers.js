import {ref, computed} from 'vue'

export function useSortedUsers(users) {
    const selectedSort = ref('');
    const sortedUsers = computed(() => {
        return [...users.value].sort((user1, user2) => user1[selectedSort.value]?.localeCompare(user2[selectedSort.value]))
    });
    return {
        selectedSort, sortedUsers
    }
};