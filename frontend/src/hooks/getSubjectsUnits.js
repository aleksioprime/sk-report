import {ref, computed} from 'vue'

export function getSubjectsUnits(units, filterQueryDepartments) {
    const subjectsUnits = computed(() => {
        if (!filterQueryDepartments.value) {
            return units.value.map((unit) => {return unit.subject.id;})
        } else {
            return units.value.map((unit) => {
                if (unit.subject.department.id == filterQueryDepartments.value) {
                    return unit.subject.id;
                }
			});
        }
    })
        
    return {
        subjectsUnits
    }
};