import {ref, computed} from 'vue'

export function filterCriteriaBySubject(criteria) {
    const querySubject = ref('');
    const filteredCriteriaBySubject = computed(() => {
        if (!querySubject.value) {
            return []
        } else {
            return criteria.value.filter((cr) => cr.subject_group.id == querySubject.value)
        }   
    });
    return {
        querySubject, filteredCriteriaBySubject
    }
};