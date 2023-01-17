import axios from "axios"

axios.defaults.baseURL = 'http://localhost:8080/api/v1/';

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true
        const {status, data} = await axios.post('token/refresh/', {
            "refresh": localStorage.getItem('refresh_token'),
        }, {
            withCredentials: true
        });
        if (status == 200) {
            axios.defaults.headers.common['Authorization'] = `Bearer ' + ${data.access}`;
            localStorage.setItem('access_token', data.access);
            return axios(error.config);
        }
    }
    refresh = false;
    return error;
})