import {ref, computed} from 'vue'

// составление списка предметов из имеющихся юнитов в выбранном отделе
export function getSubjectsUnits(units) {
    const subjectsUnits = computed(() => {
        let objArray = units.value.map((unit) => {return unit.subject})
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    })
        
    return {
        subjectsUnits
    }
};


// export function getSubjectsUnits(units, filterQueryDepartments) {
//     const subjectsUnits = computed(() => {
//         let objArray = []
//         if (!filterQueryDepartments.value) {
//             objArray = units.value.map((unit) => {return unit.subject})
//         } else {
//             objArray =  units.value.map((unit) => {
//                 if (unit.subject.department.id == filterQueryDepartments.value) {
//                     return unit.subject;
//                 }
// 			});
//         }
//         return [...new Map(objArray.map((item) => [item["id"], item])).values()]
//     })
        
//     return {
//         subjectsUnits
//     }
// };