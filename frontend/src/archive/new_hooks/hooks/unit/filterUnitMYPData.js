import { ref, computed } from 'vue'

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

// составление списка годов обучения из имеющихся юнитов
export function getSubjectsFromUnits(units) {
    const subjectsFromUnits = computed(() => {
        let objArray = units.value.map((unit) => {return unit.subject})
        return [...new Map(objArray.map((item) => [item["id"], item])).values()]
    })
        
    return {
        subjectsFromUnits
    }
};

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

export function filterTeachersByDepartment(teachers) {
    const queryDepartment = ref('');
    const filteredTeachersByDepartment = computed(() => {
        if (!queryDepartment.value) {
            return teachers.value
        } else {
            return teachers.value.filter((teacher) => {
                const teachersDepartment = teacher.departments.find(item => item.id == queryDepartment.value)
                return teachersDepartment ? true : false
            })
        }   
    });
    return {
        queryDepartment, filteredTeachersByDepartment
    }
};

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