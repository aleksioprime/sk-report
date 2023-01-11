import {computed} from 'vue'

// составление списка предметов из имеющихся юнитов
export function getSubjectsFromUnits(units) {
    const subjectsFromUnits = computed(() => {
        let objArray = units.value.map((unit) => {return unit.subject})
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    })
        
    return {
        subjectsFromUnits
    }
};