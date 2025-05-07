import { defineStore } from 'pinia';
import axios from '@/services/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        access: null,
        refresh: null,
        error: null,
        success: null,
    }),
    actions: {
        async login(username, password) {
            this.error = '';
            this.success = '';
            try {
                const res = await axios.post('/api/token/', {
                    username,
                    password,
                });
                this.error = null;
                this.refresh = res.data.refresh;
                this.access = res.data.access;
                this.success = 'تم تسجيل الدخول بنجاح 🎉';

                localStorage.setItem("access", res.data.access);
                localStorage.setItem("refresh", res.data.refresh);
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
                    // email,
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
            this.user = null;
            this.error = null;
            this.success = null;
            this.access = null;
            this.refresh = null;
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            delete axios.defaults.headers.common['Authorization'];
            window.location.href = "/auth/signin";
        },
    },
});
