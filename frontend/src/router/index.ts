import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useAppStore } from '@/stores/index';
import appSetting from '@/app-setting';


const routes: RouteRecordRaw[] = [
    // dashboard
    { path: '', name: 'home', component: () => import('../components/FormBuilder/FormList.vue') },

    {
        path: '/icons',
        name: 'icons',
        component: () => import('../views/icons.vue'),
    },
    {
        path: '/admin-form-new',
        name: 'admin-form-new',
        component: () => import('@/components/FormBuilder/FormBuilder.vue'),
    },
    {
        path: '/admin-form-edit/:id',
        name: 'admin-form-edit',
        component: () => import('../components/FormBuilder/FormBuilder.vue'),
        props: true,
    },
    {
        path: '/forms',
        name: 'forms',
        component: () => import('../components/FormBuilder/FormList.vue'),
    },

    {
        path: '/submissions/:formId',
        name: 'submissions-id',
        component: () => import('@/components/FormBuilder/SubmissionList.vue'),
        props: true,
    },
    {
        path: '/submissions',
        name: 'submissions',
        component: () => import('@/components/FormBuilder/SubmissionList.vue'),
    },

    {
        path: '/submissions/:formId/new',
        name: 'submissions-new',
        component: () => import('@/components/FormBuilder/SubmissionForm.vue'),
        props: true,
    },
    {
        path: '/submissions/:formId/:id',
        name: 'submissions-view',
        component: () => import('@/components/FormBuilder/SubmissionForm.vue'),
        props: true,
    },
    {
        path: '/submissions/:formId/:id/edit',
        name: 'submission-edit',
        component: () => import('@/components/FormBuilder/SubmissionForm.vue'),
        props: true,
    },
    {
        path: '/submissions/:formId/:id/edit/:tabId',
        name: 'submission-edit-tab',
        component: () => import('@/components/FormBuilder/SubmissionForm.vue'),
        props: true,
    },
    {
        path: '/submissions/:formId/:id/:tabId',
        name: 'submission-view-tab',
        component: () => import('@/components/FormBuilder/SubmissionForm.vue'),
        props: true,
    },

    // authentication
    {
        path: '/auth/signin',
        name: 'boxed-signin',
        component: () => import(/* webpackChunkName: "auth-boxed-signin" */ '../views/auth/boxed-signin.vue'),
        meta: { layout: 'auth' },
    },
    {
        path: '/auth/signup',
        name: 'boxed-signup',
        component: () => import(/* webpackChunkName: "auth-boxed-signup" */ '../views/auth/boxed-signup.vue'),
        meta: { layout: 'auth' },
    },
    {
        path: '/auth/lockscreen',
        name: 'boxed-lockscreen',
        component: () => import(/* webpackChunkName: "auth-boxed-lockscreen" */ '../views/auth/boxed-lockscreen.vue'),
        meta: { layout: 'auth' },
    },
    {
        path: '/auth/password-reset',
        name: 'boxed-password-reset',
        component: () => import(/* webpackChunkName: "auth-boxed-password-reset" */ '../views/auth/boxed-password-reset.vue'),
        meta: { layout: 'auth' },
    },
];

const router = createRouter({
    history: createWebHistory(),
    linkExactActiveClass: 'active',
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition;
        } else {
            return { left: 0, top: 0 };
        }
    },
});

router.beforeEach((to, from, next) => {
    const store = useAppStore();

    // 🔄 تغيير الواجهة حسب نوع الصفحة
    if (to?.meta?.layout == 'auth') {
        store.setMainLayout('auth');
    } else {
        store.setMainLayout('app');
    }

    // ✅ حماية الصفحات الخاصة
    const isPublicPage = to.path.startsWith('/auth');
    const accessToken = localStorage.getItem('access');

    if (!isPublicPage && !accessToken) {
        // ⛔ مفيش توكن → ورايح على صفحة خاصة → رجّعه على تسجيل الدخول
        return next({ path: '/auth/signin' });
    }

    return next();
});

router.afterEach((to, from, next) => {
    appSetting.changeAnimation();
});
export default router;
