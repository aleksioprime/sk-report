import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getSubjects() {
  const subjects = ref([]);
  const fetchGetSubjects = async (data) => {
    const config = {
      params: {
        department: data.department || null,
        level: data.level || null,
        type: data.type || null,
        author: data.author || null,
        teacher: data.teacher || null,
        program: data.program || null,
        need_report: data.need_report || null,
        plan: data.plan || null,
      }
    }
    await axiosAPI.get('myp/subjects', config).then((response) => {
        console.log('Получен список предметов: ', response.data)
        subjects.value = response.data;
    });
  };
  return {
    subjects, fetchGetSubjects
  }
}

export function getWorkLoadSubjects() {
  const workLoadSubjects = ref([]);
  const fetchGetWorkLoadSubjects = async (data) => {
    const config = {
      params: {
        department: data.department || null,
        study_year: data.study_year || null,
      }
    }
    await axiosAPI.get('workload/subjects', config).then((response) => {
        console.log('Получен список предметов с учебной нагрузкой: ', response.data)
        workLoadSubjects.value = response.data;
    });
  };
  return {
    workLoadSubjects, fetchGetWorkLoadSubjects
  }
}

export function getWorkLoadSubject() {
  const workLoadSubject = ref([]);
  const fetchGetWorkLoadSubject = async (id) => {
    await axiosAPI.get(`workload/subjects/${id}`).then((response) => {
        console.log('Получен предмет с учебной нагрузкой: ', response.data)
        workLoadSubject.value = response.data;
    });
  };
  return {
    workLoadSubject, fetchGetWorkLoadSubject
  }
}