<template>
    <div :class="{ 'dark text-white-dark': store.semidark }">
        <nav class="sidebar fixed min-h-screen h-full top-0 bottom-0 w-[260px] xxxs:w-[160px] shadow-[5px_0_25px_0_rgba(94,92,154,0.1)] z-50 transition-all duration-300">
            <div class="bg-white dark:bg-[#0e1726] h-full">
                <div class="flex justify-between items-center px-4 py-3">
                    <router-link to="/" class="main-logo flex items-center shrink-0">
                        <img class="w-8 ml-[5px] flex-none" src="/assets/images/logo.png" alt="" />
                        <span class="text-2xl ltr:ml-1.5 rtl:mr-1.5 font-semibold align-middle lg:inline dark:text-white-light">HNU</span>
                    </router-link>
                    <a
                        href="javascript:;"
                        class="collapse-icon w-8 h-8 rounded-full flex items-center hover:bg-gray-500/10 dark:hover:bg-dark-light/10 dark:text-white-light transition duration-300 rtl:rotate-180 hover:text-primary"
                        @click="store.toggleSidebar()"
                    >
                        <icon-carets-down class="m-auto rotate-90" />
                    </a>
                </div>
                <perfect-scrollbar
                    :options="{
                        swipeEasing: true,
                        wheelPropagation: false,
                    }"
                    class="h-[calc(100vh-80px)] relative"
                >
                    <ul class="relative font-semibold space-y-0.5 p-4 py-0">
                        <p v-if="!menuTree.length">{{ menuTree.length }}جاري تحميل القائمة...</p>
                        <div v-else v-for="section in menuTree" :key="section.id">
                            <h2 class="py-3 px-7 flex items-center uppercase font-extrabold bg-white-light/30 dark:bg-dark dark:bg-opacity-[0.08] -mx-4 mb-1">
                                <icon-minus class="w-4 h-5 flex-none hidden" />
                                <span>{{ section.name}}</span>
                            </h2>
                            <div v-for="section2 in section.children" :key="section2.id">
                                <li v-if="section2.children.length > 0" class="menu nav-item">
                                    <button
                                        type="button"
                                        class="nav-link group w-full"
                                        :class="{ active: activeDropdown === section2.id }"
                                        @click="activeDropdown === section2.id ? (activeDropdown = null) : (activeDropdown = section2.id)"
                                    >
                                        <div class="flex items-center">
                                            <!-- <icon-menu-dashboard class="group-hover:!text-primary shrink-0" /> -->
                                            <!-- <component :is="iconComponents[section2.icon]" class="group-hover:!text-primary shrink-0" /> -->
                                            <component :is="icons[section2.icon]" class="group-hover:!text-primary shrink-0" />
                                            <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">{{
                                                section2.name
                                            }}</span>
                                        </div>
                                        <div :class="{ 'rtl:rotate-90 -rotate-90': activeDropdown !== section2.id }">
                                            <icon-caret-down />
                                        </div>
                                    </button>
                                    <vue-collapsible :isOpen="activeDropdown === section2.id">
                                        <ul class="sub-menu text-gray-500">
                                            <li v-for="section3 in section2.children" :key="section3.id">
                                                <router-link :to="section3.to" @click="toggleMobileMenu">{{ section3.name }}</router-link>
                                            </li>
                                        </ul>
                                    </vue-collapsible>
                                </li>
                                <li v-else class="menu nav-item">
                                    <router-link :to="section2.to" class="nav-link group" @click="toggleMobileMenu">
                                        <div class="flex items-center">
                                            <!-- <component :is="iconComponents[section2.icon]" class="group-hover:!text-primary shrink-0" /> -->
                                            <component :is="icons[section2.icon]" class="group-hover:!text-primary shrink-0" />

                                            <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">{{
                                                section2.name
                                            }}</span>
                                        </div>
                                    </router-link>
                                </li>
                            </div>
                        </div>
                    </ul>
                </perfect-scrollbar>
            </div>
        </nav>
    </div>
</template>

<script lang="ts" setup>
    import { ref, onMounted ,computed} from 'vue';
    import axios from '@/services/axios';
    import { useAppStore } from '@/stores/index';
    import VueCollapsible from 'vue-height-collapsible/vue3';

    const modules = import.meta.glob('@/components/icon/**/*.vue', { eager: true });

    const icons: Record<string, any> = {};
    for (const path in modules) {
        const shortName = path.split('/').pop()?.replace('.vue', '') || '';
        icons[shortName] = (modules[path] as any).default;
    }

    import IconCaretsDown from '@/components/icon/icon-carets-down.vue';
    import IconMenuDashboard from '@/components/icon/menu/icon-menu-dashboard.vue';
    import IconMinus from '@/components/icon/icon-minus.vue';
    import IconMenuChat from '@/components/icon/menu/icon-menu-chat.vue';
    import IconMenuMailbox from '@/components/icon/menu/icon-menu-mailbox.vue';
    import IconMenuTodo from '@/components/icon/menu/icon-menu-todo.vue';
    import IconMenuNotes from '@/components/icon/menu/icon-menu-notes.vue';
    import IconMenuScrumboard from '@/components/icon/menu/icon-menu-scrumboard.vue';
    import IconMenuContacts from '@/components/icon/menu/icon-menu-contacts.vue';
    import IconMenuInvoice from '@/components/icon/menu/icon-menu-invoice.vue';
    import IconCaretDown from '@/components/icon/icon-caret-down.vue';
    import IconMenuCalendar from '@/components/icon/menu/icon-menu-calendar.vue';
    import IconMenuComponents from '@/components/icon/menu/icon-menu-components.vue';
    import IconMenuElements from '@/components/icon/menu/icon-menu-elements.vue';
    import IconMenuCharts from '@/components/icon/menu/icon-menu-charts.vue';
    import IconMenuWidgets from '@/components/icon/menu/icon-menu-widgets.vue';
    import IconMenuFontIcons from '@/components/icon/menu/icon-menu-font-icons.vue';
    import IconMenuDragAndDrop from '@/components/icon/menu/icon-menu-drag-and-drop.vue';
    import IconMenuTables from '@/components/icon/menu/icon-menu-tables.vue';
    import IconMenuDatatables from '@/components/icon/menu/icon-menu-datatables.vue';
    import IconMenuForms from '@/components/icon/menu/icon-menu-forms.vue';
    import IconMenuUsers from '@/components/icon/menu/icon-menu-users.vue';
    import IconMenuPages from '@/components/icon/menu/icon-menu-pages.vue';
    import IconMenuAuthentication from '@/components/icon/menu/icon-menu-authentication.vue';
    import IconMenuDocumentation from '@/components/icon/menu/icon-menu-documentation.vue';

    const iconComponents = {
        IconMenuDashboard,
        IconMenuChat,
        IconMenuMailbox,
        IconMenuTodo,
        IconMenuNotes,
        IconMenuScrumboard,
        IconMenuContacts,
        IconMenuInvoice,
        IconMenuCalendar,
        IconMenuComponents,
        IconMenuElements,
        IconMenuCharts,
        IconMenuWidgets,
        IconMenuFontIcons,
        IconMenuDragAndDrop,
        IconMenuTables,
        IconMenuDatatables,
        IconMenuForms,
        IconMenuUsers,
        IconMenuPages,
        IconMenuAuthentication,
        IconMenuDocumentation,
    };
 

    const store = useAppStore();
    const activeDropdown: any = ref('');
    const subActive: any = ref('');
    const is_staff = localStorage.getItem('user_is_staff') ==="true"
    const menuTree = ref<any[]>([]);

    const fetchSubmission = async () => {
        try {
            if (is_staff) {
                const response = await axios.get(`/media/staff_menu.json`);
                menuTree.value = response.data;
                
            }
            else{
                const response = await axios.get(`/media/user_menu.json`);
                menuTree.value = response.data;

            }
        } catch (error) {
            console.error('Error fetching submission', error);
        }
    };
    onMounted(fetchSubmission);

    onMounted(() => {
        const selector = document.querySelector('.sidebar ul a[href="' + window.location.pathname + '"]');
        if (selector) {
            selector.classList.add('active');
            const ul: any = selector.closest('ul.sub-menu');
            if (ul) {
                let ele: any = ul.closest('li.menu').querySelectorAll('.nav-link') || [];
                if (ele.length) {
                    ele = ele[0];
                    setTimeout(() => {
                        ele.click();
                    });
                }
            }
        }
    });

    const toggleMobileMenu = () => {
        if (window.innerWidth < 1024) {
            store.toggleSidebar();
        }
    };
</script>
