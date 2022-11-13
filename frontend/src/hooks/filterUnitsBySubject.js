import {ref, computed} from 'vue'

export function filterUnitsBySubject(units) {
    const filterQuerySubject = ref('');
    const filteredUnitsBySubject = computed(() => {
        if (!filterQuerySubject.value) {
            return units.value
        } else {
            return units.value.filter(unit => unit.subject.id == filterQuerySubject.value);
        }   
    });
    return {
        filterQuerySubject, filteredUnitsBySubject
    }
};