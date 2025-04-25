import { defineStore } from 'pinia';
import axios from '@/services/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: null,
        error: null,
        success: null,
    }),
    actions: {
        async login(username, password) {
            try {
                const res = await axios.post('/api/token/', {
                    username,
                    password,
                });
                this.token = res.data.access;
                this.error = null;
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
                localStorage.setItem('token', this.token);
            } catch {
                this.error = 'بيانات الدخول غير صحيحة';
            }
        },
        async signup(username, email, password) {
            this.error = '';
            this.success = '';
            try {
                const res = await axios.post('/api/users/signup/', {
                    username,
                    email,
                    password,
                });
                this.success = 'تم إنشاء الحساب بنجاح 🎉';
                this.error = null;
            } catch (err) {
                this.error = err.response?.data?.error || 'حدث خطأ أثناء إنشاء الحساب';
                this.success = null;
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            this.error = null;
            this.success = null;
            localStorage.removeItem('token');
            delete axios.defaults.headers.common['Authorization'];
        },
    },
});
