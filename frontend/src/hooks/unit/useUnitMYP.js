import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getUnitsMYP() {
  const unitsMYP = ref([]);
  const isUnitLoading = ref(true)
  const totalPages = ref(1)
  const totalUnits = ref(1)
  const fetchGetUnitsMYP = async (data) => {
    const limit = data.limit || 1;
    const config = {
      params: {
        department: data.department || null,
        teacher: data.teacher || null,
        subject: data.subject || null,
        years: data.years || null,
      }
    }
    isUnitLoading.value = true;
    await axiosAPI.get('/myp/unit', config).then((response) => {
      console.log('Получен список юнитов: ', response.data)
      unitsMYP.value = response.data.results;
      totalUnits.value = response.data.count
      totalPages.value = Math.ceil(totalUnits.value / limit);
    }).finally(() => {
      isUnitLoading.value = false;
    });
  };
  return {
    unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP
  }
}

export function getUnitMYP() {
  const unitMYP = ref([]);
  const isUnitLoading = ref(true)
  const fetchGetUnitMYP = async (id) => {
    isUnitLoading.value = true;
    await axiosAPI.get(`/myp/unit/${id}`).then((response) => {
      console.log('Получены данные юнита: ', response.data)
      unitMYP.value = response.data;
    }).finally(() => {
      isUnitLoading.value = false;
    });
  };
  return {
    unitMYP, isUnitLoading, fetchGetUnitMYP
  }
}

export function createUnitMYP() {
  const createdUnitMYP = ref({});
  const fetchCreateUnitMYP = async (unit) => {
    await axiosAPI.post('/myp/unit', unit).then((response) => {
      console.log('Юнит успешно создан');
      createdUnitMYP.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    createdUnitMYP, fetchCreateUnitMYP
  }
}

export function updateUnitMYP() {
  const updatedUnitMYP = ref({});
  const fetchUpdateUnitMYP = async (id, unit) => {
    await axiosAPI.put(`/myp/unit/${id}`, unit).then((response) => {
      console.log('Юнит успешно обновлён');
      updatedUnitMYP.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedUnitMYP, fetchUpdateUnitMYP
  }
}

export function deleteUnitMYP() {
  const fetchDeleteUnitMYP = async (id) => {
    await axiosAPI.delete(`/myp/unit/${id}`).then((response) => {
      console.log('Юнит успешно удалён');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteUnitMYP
  }
}

export function getUnitListMYP() {
  const unitListMYP = ref([]);
  const fetchGetUnitListMYP = async (data) => {
    const config = {
      params: {
        year: data.year || null,
        subject: data.subject || null,
        interdisciplinary: data.interdisciplinary || null,
      }
    }
    await axiosAPI.get('/myp/unitlist', config).then((response) => {
      console.log('Получен список юнитов: ', response.data)
      unitListMYP.value = response.data;
    });
  };
  return {
    unitListMYP, fetchGetUnitListMYP
  }
}
