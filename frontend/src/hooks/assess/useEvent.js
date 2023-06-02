import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getEventParticipations() {
  const eventParticipations = ref([]);
  const fetchGetEventParticipations = async (data) => {
    const config = {
      params: {
        type: data.type || null,
        level: data.level || null,
        student: data.student || null,
      }
    }
    await axiosAPI.get('assessment/events', config).then((response) => {
        eventParticipations.value = response.data;
    });
  };
  return {
    eventParticipations, fetchGetEventParticipations
  }
}

export function getEventTypes() {
    const eventTypes = ref([]);
    const fetchGetEventTypes = async () => {
      await axiosAPI.get('assessment/events/types').then((response) => {
        eventTypes.value = response.data;
      });
    };
    return {
        eventTypes, fetchGetEventTypes
    }
  }
  

