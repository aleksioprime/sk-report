import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getUsers() {
  const users = ref([]);
  const isUserLoading = ref(true)
  const totalPages = ref(1)
  const totalUsers = ref(1)
  const fetchGetUsers = async (data) => {
    const limit = data.limit || 1;
    const config = {
      params: {
        role: data.role || null,
        page: data.page || null,
        search: data.search || null,
      }
    }
    isUserLoading.value = true;
    await axiosAPI.get('/user', config).then((response) => {
      console.log('Получен список пользователей: ', response.data)
      users.value = response.data.results;
      users.value.forEach((item) => {
        const difData = (new Date().getTime() - new Date(item.date_of_birth));
        item.year = Math.round(difData / (24 * 3600 * 365.25 * 1000));
      });
      totalUsers.value = response.data.count
      totalPages.value = Math.ceil(totalUsers.value / limit);
    }).finally(() => {
      isUserLoading.value = false;
    });
  };
  return {
    users, isUserLoading, totalPages, totalUsers, fetchGetUsers
  }
}


export function getTeachers() {
  const teachers = ref([]);
  const isTeacherLoading = ref(true)
  const fetchGetTeachers = async (role) => {
    const config = {
      params: {
        role: role || null,
      }
    }
    isTeacherLoading.value = true;
    await axiosAPI.get('/teachers', config).then((response) => {
      console.log('Получен список учителей: ', response.data)
      teachers.value = response.data;
    }).finally(() => {
      isTeacherLoading.value = false;
    });
  };
  return {
    teachers, isTeacherLoading, fetchGetTeachers
  }
}

export function createUser() {
  const fetchCreateUser = async (user) => {
    await axiosAPI.post('/user', user).then((response) => {
      console.log('Пользователь успешно добавлен');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchCreateUser
  }
}

export function updateUser() {
  const fetchUpdateUser = async (user) => {
    await axiosAPI.put(`/user/${user.id}`, user).then((response) => {
      console.log('Пользователь успешно обновлён');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchUpdateUser
  }
}

export function deleteUser() {
  const fetchDeleteUser = async (user) => {
    await axiosAPI.delete(`/user/${user.id}`, user).then((response) => {
      console.log('Пользователь успешно удалён');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteUser
  }
}

export function archiveUser() {
  const fetchArchiveUser = async (user) => {
    user.is_active = false;
    await axiosAPI.put(`/user/${user.id}`, user).then((response) => {
      console.log('Пользователь успешно отправлен в архив');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchArchiveUser
  }
}

export function importUsers() {
  const isUserNewLoading = ref(false)
  const usersUpdated = ref([]);
  const totalNewPages = ref(1)
  const totalNewUsers = ref(1)
  const fetchImportUsers = async (data, limit) => {
    const newLimit = limit || 1;
    isUserNewLoading.value = true;
    await axiosAPI.post('/user/import', data).then((response) => {
      console.log('Пользователи успешно импортированы');
      usersUpdated.value = response.data.results;
      usersUpdated.value.forEach((item) => {
        const difData = (new Date().getTime() - new Date(item.date_of_birth));
        item.year = Math.round(difData / (24 * 3600 * 365.25 * 1000));
      });
      totalNewUsers.value = response.data.count
      totalNewPages.value = Math.ceil(totalNewUsers.value / newLimit);
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    }).finally(() => {
      isUserNewLoading.value = false;
    });
  };
  return {
    usersUpdated, isUserNewLoading, totalNewPages, totalNewUsers, fetchImportUsers
  }
}