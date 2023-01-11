import {ref, computed} from 'vue'

export function filterUnitsByYears(units) {
    const queryYears = ref([]);
    const filteredUnitsByYears = computed(() => {
        if (queryYears.value.length) {
            return units.value.filter(unit => queryYears.value.map(item => item.id).includes(unit.class_year.id));
        }
        return units.value
    });
    return {
        queryYears, filteredUnitsByYears
    }
};