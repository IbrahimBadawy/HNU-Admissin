<template>
    <!--  BEGIN MAIN CONTAINER  -->
    <div class="relative">
        <!-- sidebar menu overlay -->
        <div class="fixed inset-0 bg-[black]/60 z-50 lg:hidden" :class="{ hidden: !store.sidebar }"
            @click="store.toggleSidebar()"></div>

        <!-- screen loader -->
        <div v-show="store.isShowMainLoader"
            class="screen_loader fixed inset-0 bg-[#fafafa] dark:bg-[#060818] z-[60] grid place-content-center animate__animated">
            <img src="/assets/images/logo.png" alt="Logo" class="w-32 h-32 animate-pulse" />

        </div>

        <div class="fixed bottom-6 ltr:right-6 rtl:left-6 z-50">
            <template v-if="showTopButton">
                <button type="button"
                    class="btn btn-outline-primary rounded-full p-2 animate-pulse bg-[#fafafa] dark:bg-[#060818] dark:hover:bg-primary"
                    @click="goToTop">
                    <svg width="24" height="24" class="h-4 w-4" viewBox="0 0 24 24" fill="none"
                        xmlns="http://www.w3.org/2000/svg">
                        <path opacity="0.5" fill-rule="evenodd" clip-rule="evenodd"
                            d="M12 20.75C12.4142 20.75 12.75 20.4142 12.75 20L12.75 10.75L11.25 10.75L11.25 20C11.25 20.4142 11.5858 20.75 12 20.75Z"
                            fill="currentColor" />
                        <path
                            d="M6.00002 10.75C5.69667 10.75 5.4232 10.5673 5.30711 10.287C5.19103 10.0068 5.25519 9.68417 5.46969 9.46967L11.4697 3.46967C11.6103 3.32902 11.8011 3.25 12 3.25C12.1989 3.25 12.3897 3.32902 12.5304 3.46967L18.5304 9.46967C18.7449 9.68417 18.809 10.0068 18.6929 10.287C18.5768 10.5673 18.3034 10.75 18 10.75L6.00002 10.75Z"
                            fill="currentColor" />
                    </svg>
                </button>
            </template>
        </div>

        <!-- BEGIN APP SETTING LAUNCHER -->
        <!-- <Setting /> -->
        <!-- END APP SETTING LAUNCHER -->

        <div class="main-container text-black dark:text-white-dark min-h-screen" :class="[store.navbar]">
            <!--  BEGIN SIDEBAR  -->
            <Sidebar />
            <!--  END SIDEBAR  -->

            <div class="main-content flex flex-col min-h-screen">
                <!--  BEGIN TOP NAVBAR  -->
                <Header />
                <!--  END TOP NAVBAR  -->

                <!--  BEGIN CONTENT AREA  -->
                <div class="p-6 animation">
                    <router-view></router-view>
                </div>
                <!--  END CONTENT AREA  -->

                <!-- BEGIN FOOTER -->
                <Footer />
                <!-- END FOOTER -->
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Sidebar from '@/components/layout/Sidebar.vue';
import Header from '@/components/layout/Header.vue';
import Footer from '@/components/layout/Footer.vue';
import Setting from '@/components/ThemeCustomizer.vue';
import appSetting from '@/app-setting';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

import { useAppStore } from '@/stores/index';
const store = useAppStore();
const showTopButton = ref(false);
const authStore = useAuthStore();
const router = useRouter();
onMounted(() => {
    window.onscroll = () => {
        if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
            showTopButton.value = true;
        } else {
            showTopButton.value = false;
        }
    };

    const eleanimation: any = document.querySelector('.animation');
    eleanimation.addEventListener('animationend', function () {
        appSetting.changeAnimation('remove');
    });
    store.toggleMainLoader();
});

const goToTop = () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
};
</script>
