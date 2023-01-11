import {ref, computed} from 'vue'

export function filterUnitsBySubject(units) {
    const querySubject = ref('');
    const filteredUnitsBySubject = computed(() => {
        if (querySubject.value) {
            return units.value.filter(unit => unit.subject.id == querySubject.value.id);
        }  
        return units.value
    });
    return {
        querySubject, filteredUnitsBySubject
    }
};