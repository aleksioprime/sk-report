import {ref, computed} from 'vue'

export function filterUnitsByDepartment(units, filterQueryDepartments) {
    const filteredUnitsByDepartment = computed(() => {
        if (!filterQueryDepartments.value) {
            return units.value
        } else {
            return units.value.filter((unit) => {
                return unit.subject.department.id == filterQueryDepartments.value
            })
        }   
    });
    return {
        filteredUnitsByDepartment
    }
};