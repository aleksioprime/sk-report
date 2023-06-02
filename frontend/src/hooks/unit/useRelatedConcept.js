import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getRelatedConcepts() {
  const relatedConcepts = ref([]);
  const fetchGetRelatedConcepts = async (data) => {
    const config = {
      params: {
			  subject: data.subject || null,
        subjects: data.subjects || null,
      }
		};
    await axiosAPI.get('myp/rconcepts', config).then((response) => {
      relatedConcepts.value = response.data;
    });
  };
  return {
    relatedConcepts, fetchGetRelatedConcepts
  }
}
