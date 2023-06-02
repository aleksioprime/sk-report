import { ref, computed } from 'vue'


// export function getTeachersFromDepartment(departments) {
//     const queryDepartment = ref('');
//     const teachersFromDepartment = computed(() => {
//         if (!queryDepartment.value) {
//             let teacherDepartments = departments.value.filter(dp => dp.teacher.length > 0).map(dp => dp.teacher).flat();
//             return [...new Map(teacherDepartments.map((item) => [item["id"], item])).values()]
//         } else {
//             return departments.value.find((item => item.id == queryDepartment.value)).teacher
//         }
//     });
//     return {
//         queryDepartment, teachersFromDepartment
//     }
// };

export function getSubjectsFromDepartment(departments) {
    const queryDepartment = ref('');
    const subjectsFromDepartment = computed(() => {
        if (!queryDepartment.value) {
            let subjectDepartments = departments.value.filter(dp => dp.subject.length > 0).map(dp => dp.subject).flat();
            return [...new Map(subjectDepartments.map((item) => [item["id"], item])).values()]
        } else {
            return departments.value.find((item => item.id == queryDepartment.value)).subject
        }
    })
    return {
        subjectsFromDepartment, queryDepartment
    }
};

export function getSubjectsFromTeacher() {
    const subjectsFromTeacher = (teacher) => {
        if (teacher) {
            let subjectTeacher = teacher.teacher.units.map(un => un.subjects).flat().map(sb => sb.subject);
            return [...new Map(subjectTeacher.map((item) => [item["id"], item])).values()]
        } else {
            return []
        }
        
    }
    return {
        subjectsFromTeacher
    }
};

export function getYearsFromUnits(units) {
    const yearsFromUnits = computed(() => {
        let objArray = units.value.map((unit) => { return unit.class_year });
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    })
    return {
        yearsFromUnits
    }
};

export function filterUnitsByYears(units) {
    const queryYears = ref([]);
    const filteredUnitsByYears = computed(() => {
        return units.value.filter(unit => queryYears.value.map(item => item.id).includes(unit.class_year.id));
    });
    return {
        queryYears, filteredUnitsByYears
    }
};

export function filterCriteriaBySubject(criteria) {
    const querySubjects = ref([]);
    const filteredCriteriaBySubject = computed(() => {
        if (!querySubjects.value.length) {
            return []
        } else {
            return criteria.value.filter(cr => querySubjects.value.includes(cr.subject_group.id))
        }   
    });
    return {
        querySubjects, filteredCriteriaBySubject
    }
};