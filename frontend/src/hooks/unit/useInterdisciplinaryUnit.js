import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getInterdisciplinaryUnits() {
  const interdisciplinaryUnits = ref([]);
  const fetchGetInterdisciplinaryUnits = async (data) => {
    const config = {
      params: {
			  class_year: data.class_year || null,
      }
		};
    await axiosAPI.get('myp/interdisciplinary', config).then((response) => {
      interdisciplinaryUnits.value = response.data;
    });
  };
  return {
    interdisciplinaryUnits, fetchGetInterdisciplinaryUnits
  }
}

export function getInterdisciplinaryUnit() {
  const interdisciplinaryUnit = ref([]);
  const isUnitIDLoading = ref(true)
  const fetchGetInterdisciplinaryUnit = async (id) => {
    isUnitIDLoading.value = true;
    await axiosAPI.get(`/myp/interdisciplinary/${id}`).then((response) => {
      console.log('Получены данные юнита: ', response.data)
      interdisciplinaryUnit.value = response.data;
    }).finally(() => {
      isUnitIDLoading.value = false;
    });
  };
  return {
    interdisciplinaryUnit, isUnitIDLoading, fetchGetInterdisciplinaryUnit
  }
}

export function createInterdisciplinaryUnit() {
  const interdisciplinaryUnit = ref({});
  const fetchCreateInterdisciplinaryUnit = async (unit) => {
    await axiosAPI.post('/myp/interdisciplinary', unit).then((response) => {
      console.log('Юнит успешно создан');
      interdisciplinaryUnit.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    interdisciplinaryUnit, fetchCreateInterdisciplinaryUnit
  }
}

export function updateInterdisciplinaryUnit() {
  const updatedInterdisciplinaryUnit = ref({});
  const fetchUpdateInterdisciplinaryUnit = async (id, unit) => {
    await axiosAPI.put(`/myp/interdisciplinary/${id}`, unit).then((response) => {
      console.log('Юнит успешно обновлён');
      updatedInterdisciplinaryUnit.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedInterdisciplinaryUnit, fetchUpdateInterdisciplinaryUnit
  }
}

export function deleteInterdisciplinaryUnit() {
  const fetchDeleteInterdisciplinaryUnit = async (id) => {
    await axiosAPI.delete(`/myp/interdisciplinary/${id}`).then((response) => {
      console.log('Юнит успешно удален');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteInterdisciplinaryUnit
  }
}