import {ref, computed} from 'vue'

export function filterUnitsByYear(units) {
    const filterQueryYear = ref([]);
    const filteredUnitsByYear = computed(() => {
        if (!filterQueryYear.value) {
            return units.value
        } else {
            return units.value.filter(unit => filterQueryYear.value.includes(unit.class_year.id));
        }   
    });
    return {
        filterQueryYear, filteredUnitsByYear
    }
};