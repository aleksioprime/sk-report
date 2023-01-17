import {computed} from 'vue'

// составление списка годов обучения из имеющихся юнитов
export function getYearsFromUnits(units) {
    const yearsFromUnits = computed(() => {
        let objArray = units.value.map((unit) => { return unit.class_year });
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    })
    return {
        yearsFromUnits
    }
};