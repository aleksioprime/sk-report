import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getSummativeWorks() {
	const summativeWorks = ref([]);
  	const isSumWorkLoading = ref(true);
	const fetchGetSummativeWorks = async (data) => {
		const config = {
			params: {
				teacher: data.teacher || "",
				period: data.period || "",
			}
		}
    isSumWorkLoading.value = true;
		await axiosAPI.get('/assessment/sumwork', config).then((response) => {
			console.log("Загрузка итоговых работ")
			summativeWorks.value = response.data;
			console.log(summativeWorks.value)
		}).finally(() => {
      isSumWorkLoading.value = false;
    });
	};
	return {
		summativeWorks, isSumWorkLoading, fetchGetSummativeWorks
	}
}

export function getSummativeWorkGroup() {
	const summativeWorkGroup = ref({
    work: {
			criteria: []
		},
		students: []
  });
  const isWorkGroupLoading = ref(true);
	const fetchGetSummativeWorkGroup = async (id) => {
    isWorkGroupLoading.value = true;
		await axiosAPI.get(`/assessment/workgroup/${id}`).then((response) => {
			console.log("Загрузка группы итоговой работы")
			summativeWorkGroup.value = response.data;
			console.log(summativeWorkGroup.value)
		}).finally(() => {
      isWorkGroupLoading.value = false;
    });
	};
	return {
		summativeWorkGroup, isWorkGroupLoading, fetchGetSummativeWorkGroup
	}
}


export function createSummativeWork() {
	const createdSummativeWork = ref({});
	const fetchCreateSummativeWork = async (unit) => {
	  await axiosAPI.post('/assessment/sumwork', unit).then((response) => {
		console.log('Итоговая работа успешно создана');
		createdSummativeWork.value = response.data
	  }).catch((error) => {
		console.log('Ошибка запроса: ', error);
	  });
	};
	return {
	  createdSummativeWork, fetchCreateSummativeWork
	}
}

export function updateSummativeWork() {
  const updatedSummativeWork = ref({});
  const fetchUpdateSummativeWork = async (id, unit) => {
    await axiosAPI.put(`/assessment/sumwork/${id}`, unit).then((response) => {
      console.log('Итоговая работа успешно обновлена');
      updatedSummativeWork.value = response.data
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedSummativeWork, fetchUpdateSummativeWork
  }
}

export function deleteSummativeWork() {
  const fetchDeleteSummativeWork = async (id) => {
    await axiosAPI.delete(`/assessment/sumwork/${id}`).then((response) => {
      console.log('Итоговая работа успешно удалена');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteSummativeWork
  }
}