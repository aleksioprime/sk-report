import {ref, computed} from 'vue'

export function getYearsUnits(units) {
    const yearsUnits = computed(() => {
        return units.value.map((unit) => {
            return unit.class_year.id;
        });
    })
    return {
        yearsUnits
    }
};