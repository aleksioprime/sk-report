import {ref, computed} from 'vue'

export function filterUnitsByTeachers(units) {
    const filterQueryTeachers = ref('');
    const filteredUnitsByTeachers = computed(() => {
        if (!filterQueryTeachers.value) {
            return units.value
        } else {
            return units.value.filter((unit) => {
                const unitAuthor = unit.authors.find(item => item.id == filterQueryTeachers.value)
                return unitAuthor ? true : false
            })
        }   
    });
    return {
        filterQueryTeachers, filteredUnitsByTeachers
    }
};