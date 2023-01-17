import {ref, computed} from 'vue'

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