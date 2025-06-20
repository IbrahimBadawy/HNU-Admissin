<template>
    <header class="z-40" :class="{ dark: store.semidark && store.menu === 'horizontal' }">
        <div class="shadow-sm">
            <div class="relative bg-white flex w-full items-center px-5 py-2.5 dark:bg-[#0e1726]">
                <div class="horizontal-logo flex lg:hidden justify-between items-center ltr:mr-2 rtl:ml-2">
                    <router-link to="/" class="main-logo flex items-center shrink-0">
                        <img class="w-8 ltr:-ml-1 rtl:-mr-1 inline" src="/assets/images/logo.png" alt="" />
                        <span
                            class="text-2xl ltr:ml-1.5 rtl:mr-1.5 font-semibold align-middle hidden md:inline dark:text-white-light transition-all duration-300">HNU</span>
                    </router-link>

                    <a href="javascript:;"
                        class="collapse-icon flex-none dark:text-[#d0d2d6] hover:text-primary dark:hover:text-primary flex lg:hidden ltr:ml-2 rtl:mr-2 p-2 rounded-full bg-white-light/40 dark:bg-dark/40 hover:bg-white-light/90 dark:hover:bg-dark/60"
                        @click="store.toggleSidebar()">
                        <icon-menu class="w-5 h-5" />
                    </a>
                </div>

                <div
                    class="sm:flex-1 ltr:sm:ml-0 ltr:ml-auto sm:rtl:mr-0 rtl:mr-auto flex items-center space-x-1.5 lg:space-x-2 rtl:space-x-reverse dark:text-[#d0d2d6]">
                    <div class="hidden sm:block sm:ltr:mr-auto sm:rtl:ml-auto">منصة التقديم لجامعة حلوان الأهلية</div>



                    <div class="flex shrink-0">
                        <a href="#" class="text-danger !py-3 flex items-center" @click.prevent="visible = true">
                            <icon-menu-authentication class="w-4.5 h-4.5 ltr:mr-2 rtl:ml-2  shrink-0" />
                        </a>
                        <a v-if="is_staff" href="#" class="text-danger !py-3 flex items-center" @click.prevent="visible2 = true">
                            <icon-menu-authentication class="w-4.5 h-4.5 ltr:mr-2 rtl:ml-2 rotate-90 shrink-0" />
                        </a>
                        <a href="#" class="text-danger !py-3 flex items-center" @click.prevent="handleLogOut">
                            <icon-logout class="w-4.5 h-4.5 ltr:mr-2 rtl:ml-2 rotate-90 shrink-0" />
                            الخروج
                        </a>

                    </div>
                    <Dialog v-model:visible="visible" modal header="تغيير كلمة المرور" :style="{ width: '25rem' }">
                        <span class="text-surface-500 dark:text-surface-400 block mb-8">ادخل كلمة المرور الجديدة</span>

                        <div class="flex items-center gap-4 mb-8">
                            <label for="password" class="font-semibold w-24">كلمة المرور</label>
                            <InputText v-model="password" id="password" class="flex-auto" autocomplete="off" />
                        </div>
                        <div class="flex justify-end gap-2">
                            <Button type="button" label="الغاء" severity="secondary" @click="visible = false"></Button>
                            <Button type="button" label="حفظ" @click="set_user_password"></Button>
                        </div>
                    </Dialog>

                    <Dialog v-model:visible="visible2" modal header="تغيير كلمة المرور للمستخدمين" :style="{ width: '25rem' }">
                        <span class="text-surface-500 dark:text-surface-400 block mb-8">ادخل الرقم القومي و كلمة المرور الجديدة</span>

                        <div class="flex items-center gap-4 mb-8">
                            <label for="username2" class="font-semibold w-24">الرقم القومي</label>
                            <InputText v-model="user_identifier2" id="username2" class="flex-auto" autocomplete="off" />
                        </div>
                        <div class="flex items-center gap-4 mb-8">
                            <label for="password2" class="font-semibold w-24">كلمة المرور</label>
                            <InputText v-model="password2" id="password2" class="flex-auto" autocomplete="off" />
                        </div>
                        <div class="flex justify-end gap-2">
                            <Button type="button" label="الغاء" severity="secondary" @click="visible2 = false"></Button>
                            <Button type="button" label="حفظ" @click="set_user_password2"></Button>
                        </div>
                    </Dialog>

                </div>
            </div>
        </div>
    </header>
</template>

<script  setup>
import { ref, onMounted, computed, reactive, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import appSetting from '@/app-setting';

import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/index';
import { useAuthStore } from '@/stores/auth';

import IconMenu from '@/components/icon/icon-menu.vue';

import IconLogout from '@/components/icon/icon-logout.vue';
import iconMenuAuthentication from '@/components/icon/menu/icon-menu-authentication.vue';
import axios from '@/services/axios';


const store = useAppStore();
const route = useRoute();
const search = ref(false);
const router = useRouter();
const authStore = useAuthStore();
// multi language
const i18n = reactive(useI18n());
const changeLanguage = (item) => {
    i18n.locale = item.code;
    appSetting.toggleLanguage(item);
};
const visible = ref(false);
const visible2 = ref(false);
const password = ref('');
const user_identifier2 = ref('');
const password2 = ref('');

const set_user_password = async () => {
    visible.value = false
    const user_identifier = localStorage.getItem('user_username')
    if (!user_identifier) return;
    // console.log(user_identifier)

    try {
        const res = await axios.post(`api/users/set_user_password/`, {
            username: user_identifier,
            password: password.value,
        });

        // console.log(res.data) 🗝️
        const success = res.data.success
        if (success) {
            alert("تم استعادة كلمة المرور بنجاح");
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            delete axios.defaults.headers.common['Authorization'];
            window.location.href = "/auth/signin";
        }
        const error = res.data.error
        if (error) { alert('فشل تغيير كلمة المرور'); }
    } catch (err) {
        console.error(err)
        alert('فشل تغيير كلمة المرور');
    }
};

const is_staff = computed(() => {
    const is_staff2 = JSON.parse(localStorage.getItem('user_is_staff'));
    return is_staff2;
});

const set_user_password2 = async () => {
    visible2.value = false
    if (!user_identifier2.value) return;
    // console.log(user_identifier)

    try {
        const res = await axios.post(`api/users/set_user_password/`, {
            username: user_identifier2.value,
            password: password2.value,
        });

        // console.log(res.data) 🗝️
        const success = res.data.success
        if (success) {
            alert("تم استعادة كلمة المرور بنجاح");
            user_identifier2.value=''
            password2.value=''
        }
        const error = res.data.error
        if (error) { alert('فشل تغيير كلمة المرور'); }
    } catch (err) {
        console.error(err)
        alert('فشل تغيير كلمة المرور');
    }
};

const handleLogOut = async () => {
    await authStore.logout();
    if (!authStore.access) {
        router.push('/auth/signin'); // غيّر المسار حسب المطلوب
    }
};


</script>
