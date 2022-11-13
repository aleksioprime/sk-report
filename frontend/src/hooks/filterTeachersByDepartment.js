import {ref, computed} from 'vue'

export function filterTeachersByDepartment(teachers) {
    const filterQueryDepartments = ref('');
    const filteredTeachersByDepartment = computed(() => {
        if (!filterQueryDepartments.value) {
            return teachers.value
        } else {
            return teachers.value.filter((teacher) => {
                const teachersDepartment = teacher.departments.find(item => item.id == filterQueryDepartments.value)
                return teachersDepartment ? true : false
            })
        }   
    });
    return {
        filterQueryDepartments, filteredTeachersByDepartment
    }
};