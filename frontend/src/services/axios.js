import axios from 'axios';

const instance = axios.create({
    // baseURL: 'http://localhost', // عدلها لو عندك سيرفر تاني
    baseURL: 'http://admission.hnu.edu.eg:81', // عدلها لو عندك سيرفر تاني
});

// حمل التوكن لو موجود في localStorage
const token = localStorage.getItem('token');
if (token) {
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default instance;
