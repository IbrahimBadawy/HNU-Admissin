<template>
    <div :class="{ 'dark text-white-dark': store.semidark }">
        <nav class="sidebar fixed min-h-screen h-full top-0 bottom-0 w-[260px] shadow-[5px_0_25px_0_rgba(94,92,154,0.1)] z-50 transition-all duration-300">
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
                        <li class="menu nav-item">
                            <button
                                type="button"
                                class="nav-link group w-full"
                                :class="{ active: activeDropdown === 'dashboard' }"
                                @click="activeDropdown === 'dashboard' ? (activeDropdown = null) : (activeDropdown = 'dashboard')"
                            >
                                <div class="flex items-center">
                                    <icon-menu-dashboard class="group-hover:!text-primary shrink-0" />
                                    <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">
                                        {{ $t('dashboard') }}
                                    </span>
                                </div>
                                <div :class="{ 'rtl:rotate-90 -rotate-90': activeDropdown !== 'dashboard' }">
                                    <icon-caret-down />
                                </div>
                            </button>
                            <vue-collapsible :isOpen="activeDropdown === 'dashboard'">
                                <ul class="sub-menu text-gray-500">
                                    <li>
                                        <router-link to="/" @click="toggleMobileMenu">{{ $t('sales') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/analytics" @click="toggleMobileMenu">{{ $t('analytics') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/finance" @click="toggleMobileMenu">{{ $t('finance') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/crypto" @click="toggleMobileMenu">{{ $t('crypto') }}</router-link>
                                    </li>
                                </ul>
                            </vue-collapsible>
                        </li>

                        <h2 class="py-3 px-7 flex items-center uppercase font-extrabold bg-white-light/30 dark:bg-dark dark:bg-opacity-[0.08] -mx-4 mb-1">
                            <icon-minus class="w-4 h-5 flex-none hidden" />
                            <span>{{ $t('tables_and_forms') }}</span>
                        </h2>

                        <li class="menu nav-item">
                            <router-link to="/tables" class="nav-link group" @click="toggleMobileMenu">
                                <div class="flex items-center">
                                    <icon-menu-tables class="group-hover:!text-primary shrink-0" />

                                    <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">{{ $t('tables') }}</span>
                                </div>
                            </router-link>
                        </li>

                        <li class="menu nav-item">
                            <button
                                type="button"
                                class="nav-link group w-full"
                                :class="{ active: activeDropdown === 'datatables' }"
                                @click="activeDropdown === 'datatables' ? (activeDropdown = null) : (activeDropdown = 'datatables')"
                            >
                                <div class="flex items-center">
                                    <icon-menu-datatables class="group-hover:!text-primary shrink-0" />

                                    <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">{{
                                        $t('datatables')
                                    }}</span>
                                </div>
                                <div :class="{ 'rtl:rotate-90 -rotate-90': activeDropdown !== 'datatables' }">
                                    <icon-caret-down />
                                </div>
                            </button>
                            <vue-collapsible :isOpen="activeDropdown === 'datatables'">
                                <ul class="sub-menu text-gray-500">
                                    <li>
                                        <router-link to="/datatables/basic" @click="toggleMobileMenu">{{ $t('basic') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/advanced" @click="toggleMobileMenu">{{ $t('advanced') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/skin" @click="toggleMobileMenu">{{ $t('skin') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/order-sorting" @click="toggleMobileMenu">{{ $t('order_sorting') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/columns-filter" @click="toggleMobileMenu">{{ $t('columns_filter') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/multi-column" @click="toggleMobileMenu">{{ $t('multi_column') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/multiple-tables" @click="toggleMobileMenu">{{ $t('multiple_tables') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/alt-pagination" @click="toggleMobileMenu">{{ $t('alt_pagination') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/checkbox" @click="toggleMobileMenu">{{ $t('checkbox') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/range-search" @click="toggleMobileMenu">{{ $t('range_search') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/export" @click="toggleMobileMenu">{{ $t('export') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/sticky-header" @click="toggleMobileMenu">{{ $t('sticky_header') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/clone-header" @click="toggleMobileMenu">{{ $t('clone_header') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/datatables/column-chooser" @click="toggleMobileMenu">{{ $t('column_chooser') }}</router-link>
                                    </li>
                                </ul>
                            </vue-collapsible>
                        </li>

                        <li class="menu nav-item">
                            <button
                                type="button"
                                class="nav-link group w-full"
                                :class="{ active: activeDropdown === 'forms' }"
                                @click="activeDropdown === 'forms' ? (activeDropdown = null) : (activeDropdown = 'forms')"
                            >
                                <div class="flex items-center">
                                    <icon-menu-forms class="group-hover:!text-primary shrink-0" />

                                    <span class="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">{{ $t('forms') }}</span>
                                </div>
                                <div :class="{ 'rtl:rotate-90 -rotate-90': activeDropdown !== 'forms' }">
                                    <icon-caret-down />
                                </div>
                            </button>
                            <vue-collapsible :isOpen="activeDropdown === 'forms'">
                                <ul class="sub-menu text-gray-500">
                                    <li>
                                        <router-link to="/forms/basic" @click="toggleMobileMenu">{{ $t('basic') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/input-group" @click="toggleMobileMenu">{{ $t('input_group') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/layouts" @click="toggleMobileMenu">{{ $t('layouts') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/validation" @click="toggleMobileMenu">{{ $t('validation') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/input-mask" @click="toggleMobileMenu">{{ $t('input_mask') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/select2" @click="toggleMobileMenu">{{ $t('select2') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/touchspin" @click="toggleMobileMenu">{{ $t('touchspin') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/checkbox-radio" @click="toggleMobileMenu">{{ $t('checkbox_and_radio') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/switches" @click="toggleMobileMenu">{{ $t('switches') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/wizards" @click="toggleMobileMenu">{{ $t('wizards') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/file-upload" @click="toggleMobileMenu">{{ $t('file_upload') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/quill-editor" @click="toggleMobileMenu">{{ $t('quill_editor') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/markdown-editor" @click="toggleMobileMenu">{{ $t('markdown_editor') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/date-picker" @click="toggleMobileMenu">{{ $t('date_and_range_picker') }}</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/forms/clipboard" @click="toggleMobileMenu">{{ $t('clipboard') }}</router-link>
                                    </li>
                                </ul>
                            </vue-collapsible>
                        </li>

                    </ul>
                </perfect-scrollbar>
            </div>
        </nav>
    </div>
</template>

<script lang="ts" setup>
    import { ref, onMounted } from 'vue';

    import { useAppStore } from '@/stores/index';
    import VueCollapsible from 'vue-height-collapsible/vue3';

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

    const store = useAppStore();
    const activeDropdown: any = ref('');
    const subActive: any = ref('');

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
