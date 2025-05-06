import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const instance = axios.create({
    // baseURL: 'http://localhost', // عدلها لو عندك سيرفر تاني
    baseURL: 'http://admission.hnu.edu.eg:81', // عدلها لو عندك سيرفر تاني
});

// ✅ إرفاق التوكن تلقائيًا
instance.interceptors.request.use(
    async (config) => {
        const access = localStorage.getItem('access');
        if (access) {
            config.headers.Authorization = `Bearer ${access}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ✅ محاولة تجديد التوكن تلقائيًا عند انتهاء الصلاحية
instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry && localStorage.getItem('refresh')) {
            originalRequest._retry = true;
            try {
                const refresh = localStorage.getItem('refresh');
                const res = await axios.post('/api/token/refresh/', { refresh });
                localStorage.setItem('access', res.data.access);
                instance.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
                return instance(originalRequest);
            } catch (refreshError) {
                console.error('❌ Refresh token expired');
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
                window.location.href = '/auth/signin'; // ⬅️ رجع المستخدم لصفحة الدخول
            }
        }

        return Promise.reject(error);
    }
);

export default instance;
