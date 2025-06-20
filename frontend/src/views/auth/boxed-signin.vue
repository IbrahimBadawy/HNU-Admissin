<template>
    <div>
        <div class="absolute inset-0">
            <img src="/assets/images/auth/bg-gradient.png" alt="image" class="h-full w-full object-cover" />
        </div>

        <div
            class="relative flex min-h-screen items-center justify-center bg-[url(/assets/images/auth/map.png)] bg-cover bg-center bg-no-repeat px-6 py-10 dark:bg-[#060818] sm:px-16"
        >
            <img src="/assets/images/auth/coming-soon-object1.png" alt="image" class="absolute left-0 top-1/2 h-full max-h-[893px] -translate-y-1/2" />
            <img src="/assets/images/auth/coming-soon-object2.png" alt="image" class="absolute left-24 top-0 h-40 md:left-[30%]" />
            <img src="/assets/images/auth/coming-soon-object3.png" alt="image" class="absolute right-0 top-0 h-[300px]" />
            <img src="/assets/images/auth/polygon-object.svg" alt="image" class="absolute bottom-0 end-[28%]" />
            <div
                class="relative w-full max-w-[870px] rounded-md bg-[linear-gradient(45deg,#fff9f9_0%,rgba(255,255,255,0)_25%,rgba(255,255,255,0)_75%,_#fff9f9_100%)] p-2 dark:bg-[linear-gradient(52.22deg,#0E1726_0%,rgba(14,23,38,0)_18.66%,rgba(14,23,38,0)_51.04%,rgba(14,23,38,0)_80.07%,#0E1726_100%)]"
            >
                <div class="relative flex flex-col justify-center rounded-md bg-white/60 backdrop-blur-lg dark:bg-black/50 px-6 lg:min-h-[758px] py-20">
                    <div class="mx-auto w-full max-w-[440px]">
                        <div class="mb-10">
                            <h1 class="text-3xl font-extrabold uppercase !leading-snug text-primary md:text-4xl">تسجيل الدخول</h1>
                            <p class="text-base font-bold leading-normal text-white-dark">أدخل الرقم القومي وكلمة المرور لتسجيل الدخول</p>
                        </div>
                        <form class="space-y-5 dark:text-white" @submit.prevent="handleLogin">
                            <div>
                                <label for="username">الرقم القومي</label>
                                <div class="relative text-white-dark">
                                    <input
                                        v-model="username"
                                        id="username"
                                        type="text"
                                        placeholder="أدخل الرقم القومي"
                                        class="form-input ps-10 placeholder:text-white-dark"
                                    />
                                    <span class="absolute start-4 top-1/2 -translate-y-1/2">
                                        <icon-mail :fill="true" />
                                    </span>
                                </div>
                            </div>
                            <div>
                                <label for="password">الرقم السري</label>
                                <div class="relative text-white-dark">
                                    <input
                                        v-model="password"
                                        id="password"
                                        type="password"
                                        placeholder="أدخل الرقم السري"
                                        class="form-input ps-10 placeholder:text-white-dark"
                                    />
                                    <span class="absolute start-4 top-1/2 -translate-y-1/2">
                                        <icon-lock-dots :fill="true" />
                                    </span>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-secondary !mt-6 w-full border-0 uppercase shadow-[0_10px_20px_-10px_rgba(67,97,238,0.44)]">
                                تسجيل الدخول
                            </button>
                            <p v-if="authStore.error" class="text-red-500 text-sm mt-2">{{ authStore.error }}</p>
                        </form>
                        <div class="relative my-7 text-center md:mb-9">
                            <span class="absolute inset-x-0 top-1/2 h-px w-full -translate-y-1/2 bg-white-light dark:bg-white-dark"></span>
                            <span class="relative bg-white px-2 font-bold uppercase text-white-dark dark:bg-dark dark:text-white-light">أو</span>
                        </div>

                        <div class="text-center dark:text-white">
                            ليس لديك حساب ؟
                            <router-link to="/auth/signup" class="btn btn-primary uppercase  underline transition hover:text-black dark:hover:text-white">
                                إنشاء حساب جديد
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import { ref, computed, reactive } from 'vue';
    import { useI18n } from 'vue-i18n';
    import appSetting from '@/app-setting';
    import { useAppStore } from '@/stores/index';
    import { useRouter, useRoute } from 'vue-router';
    import { useMeta } from '@/composables/use-meta';
    import { useAuthStore } from '@/stores/auth';
    import axios from '@/services/axios';

    import IconCaretDown from '@/components/icon/icon-caret-down.vue';
    import IconMail from '@/components/icon/icon-mail.vue';
    import IconLockDots from '@/components/icon/icon-lock-dots.vue';
    import IconInstagram from '@/components/icon/icon-instagram.vue';
    import IconFacebookCircle from '@/components/icon/icon-facebook-circle.vue';
    import IconTwitter from '@/components/icon/icon-twitter.vue';
    import IconGoogle from '@/components/icon/icon-google.vue';

    useMeta({ title: 'تسجيل الدخول' });
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    const store = useAppStore();
    // multi language
    const i18n = reactive(useI18n());
    const changeLanguage = (item: any) => {
        i18n.locale = item.code;
        appSetting.toggleLanguage(item);
    };

    const handleLogin = async () => {
        await authStore.login(username.value, password.value);
        if (authStore.access) {
            try {
                const res = await axios.get(`api/users/user_data/`);
                // console.log(res.data)
                localStorage.setItem('user_id', res.data.id);
                localStorage.setItem('user_is_staff', res.data.is_staff);
                localStorage.setItem('user_is_supersdmin', res.data.is_superAdmin);
                localStorage.setItem('user_username', res.data.username);
            } catch (error) {
                console.error('Error loading submissions:', error);
            } finally {
                setTimeout(() => {
                router.push('/');
            }, 100);
            }
        }
    };

    const currentFlag = computed(() => {
        return `/assets/images/flags/${i18n.locale.toUpperCase()}.svg`;
    });
</script>
