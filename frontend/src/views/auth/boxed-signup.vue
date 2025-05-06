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
                            <h1 class="text-3xl font-extrabold uppercase !leading-snug text-primary md:text-4xl">إنشاء حساب جديد</h1>
                            <p class="text-base font-bold leading-normal text-white-dark">أدخل بريدك الإلكتروني وكلمة المرور للتسجيل</p>
                        </div>
                        <form class="space-y-5 dark:text-white" @submit.prevent="handleSignup">
                            <div>
                                <label for="username">الرقم القومي</label>
                                <div class="relative text-white-dark">
                                    <input
                                        v-model="username"
                                        id="username"
                                        type="text"
                                        placeholder="ادخل الرقم القومي"
                                        class="form-input ps-10 placeholder:text-white-dark"
                                    />
                                    <span class="absolute start-4 top-1/2 -translate-y-1/2">
                                        <icon-user :fill="true" />
                                    </span>
                                </div>
                                <p v-if="nationalIdError" class="text-red-500 text-sm mt-1">{{ nationalIdError }}</p>

                            </div>
                            <div>
                                <label for="email">البريد الالكتروني</label>
                                <div class="relative text-white-dark">
                                    <input
                                        v-model="email"
                                        id="email"
                                        type="email"
                                        placeholder="أدخل بريدك الالكتروني"
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
                                        id="Password"
                                        type="password"
                                        placeholder="أدخل رقمك السري"
                                        class="form-input ps-10 placeholder:text-white-dark"
                                    />
                                    <span class="absolute start-4 top-1/2 -translate-y-1/2">
                                        <icon-lock-dots :fill="true" />
                                    </span>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary !mt-6 w-full border-0 uppercase shadow-[0_10px_20px_-10px_rgba(67,97,238,0.44)]">
                                إنشاء حساب جديد
                            </button>
                            <p v-if="authStore.error" class="text-red-500 text-sm mt-2">{{ authStore.error }}</p>
                            <p v-if="authStore.success" class="text-red-500 text-sm mt-2">{{ authStore.success }}</p>
                        </form>
                        <div class="relative my-7 text-center md:mb-9">
                            <span class="absolute inset-x-0 top-1/2 h-px w-full -translate-y-1/2 bg-white-light dark:bg-white-dark"></span>
                            <span class="relative bg-white px-2 font-bold uppercase text-white-dark dark:bg-dark dark:text-white-light">أو</span>
                        </div>

                        <div class="text-center dark:text-white">
                            لديك حساب بالفعل ؟
                            <router-link to="/auth/signin" class="btn btn-secondary uppercase underline transition hover:text-black dark:hover:text-white">
                                تسجيل الدخول
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
    import { useRouter } from 'vue-router';
    import { useMeta } from '@/composables/use-meta';
    import { useAuthStore } from '@/stores/auth';

    import IconCaretDown from '@/components/icon/icon-caret-down.vue';
    import IconUser from '@/components/icon/icon-user.vue';
    import IconMail from '@/components/icon/icon-mail.vue';
    import IconLockDots from '@/components/icon/icon-lock-dots.vue';
    import IconInstagram from '@/components/icon/icon-instagram.vue';
    import IconFacebookCircle from '@/components/icon/icon-facebook-circle.vue';
    import IconTwitter from '@/components/icon/icon-twitter.vue';
    import IconGoogle from '@/components/icon/icon-google.vue';

    const nationalIdRegex = /^(2|3)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\d{7}$/;
    const nationalIdError = ref('');

    useMeta({ title: 'انشاء حساب جديد' });
    const router = useRouter();
    const authStore = useAuthStore();

    const username = ref('');
    const email = ref('');
    const password = ref('');

    const store = useAppStore();
    // multi language
    const i18n = reactive(useI18n());
    const changeLanguage = (item: any) => {
        i18n.locale = item.code;
        appSetting.toggleLanguage(item);
    };

    const handleSignup = async () => {
        // ✅ تحقق من الرقم القومي
        if (!nationalIdRegex.test(username.value)) {
            nationalIdError.value = '❌ الرقم القومي غير صحيح';
            return;
        }

        nationalIdError.value = '';
        await authStore.signup(username.value, email.value, password.value);
        if (authStore.success) {
            setTimeout(() => {
                router.push('/auth/signin');
            }, 500);
        }
    };
    const currentFlag = computed(() => {
        return `/assets/images/flags/${i18n.locale.toUpperCase()}.svg`;
    });
</script>
