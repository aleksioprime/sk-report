import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getCriteriaGroups() {
  const criteriaGroups = ref([]);
  const fetchCriteriaGroups = async () => {
    await axiosAPI.get('curriculum/criteriagroups').then((response) => {
      criteriaGroups.value = response.data;
    });
  };
  return {
    criteriaGroups, fetchCriteriaGroups
  }
}

export function getSubjectGroups() {
  const subjectGroups = ref([]);
  const fetchSubjectGroups = async () => {
    await axiosAPI.get('curriculum/subjectgroups').then((response) => {
      subjectGroups.value = response.data;
    });
  };
  return {
    subjectGroups, fetchSubjectGroups
  }
}
