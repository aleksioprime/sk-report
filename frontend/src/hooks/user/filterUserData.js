import {ref, computed} from 'vue'

export function useSortingUsers(users) {
    const selectedSortUser = ref('');
    const sortedUsers = computed(() => {
        return [...users.value].sort((user1, user2) => user1[selectedSortUser.value]?.localeCompare(user2[selectedSortUser.value]))
    });
    return {
        selectedSortUser, sortedUsers
    }
};

export function filterUsersByLastName(users) {
    const searchLastName = ref('');
    const foundUsers = computed(() => {
        return users.value.filter(user => user.last_name.toLowerCase().includes(searchLastName.value.toLowerCase()))
    });
    return {
        searchLastName, foundUsers
    }
};

export function getRolesFromUsers(users) {
    const rolesFromUsers = computed(() => {
        let rolesUsers = users.value.filter(user => user.role.length > 0).map(user => user.role).flat();
        return [...new Map(rolesUsers.map((item) => [item["id"], item])).values()]
    });
    return {
        rolesFromUsers
    }
};