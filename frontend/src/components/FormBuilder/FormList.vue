<template>
    <div class="p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">قائمة نماذج التقديم</h2>
            <button v-if="is_staff" class="btn btn-primary" @click="goToNew">➕ نموذج جديد</button>
        </div>

        <div v-if="loading" class="text-gray-500">جاري التحميل...</div>

        <div v-else class="space-y-3">
            <div v-if="forms.value">
                <div v-for="form in forms" :key="form.id">
                    <div v-if="is_staff || (!is_staff && form.is_active)" class="flex justify-between items-center p-4 bg-white border rounded shadow">
                        <div>
                            <div class="flex items-center gap-4">
                                <div class="text-lg font-semibold">{{ form.title }}</div>
                                <div class="text-sm text-gray-500">
                                    <span
                                        @click="goToNewSubmisson(form.id)"
                                        v-if="submissions.filter((sub) => sub.form === form.id).length < form.meta_data.userSubmitCount"
                                        class="font-bold bg-blue-100 text-blue-800 px-2 py-1 rounded mr-2"
                                        >تقديم طلب جديد</span
                                    >
                                    <div v-else></div>
                                    <span
                                        @click="goToSubmissons(form.id)"
                                        v-if="submissions.filter((sub) => sub.form === form.id).length > 0"
                                        class="font-bold bg-yellow-100 text-blue-800 px-2 py-1 rounded mr-2"
                                        >تتبع حالة الطلبات</span
                                    >
                                    <span v-if="is_staff" class="font-bold bg-blue-100 text-blue-800 px-2 py-1 rounded mr-2">
                                        {{ form.submissions_count }} إجابة
                                    </span>
                                    <span v-if="is_staff" class="mr-7 text-gray-400">آخر تحديث: {{ formatDate(form.modified_at) }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="flex gap-3 text-xl items-center">
                            <!-- الحالة: تفعيل / تعطيل -->
                            <button v-if="is_staff" @click="toggleActive(form)" :title="form.is_active ? 'تعطيل' : 'تفعيل'">
                                <span v-if="form.is_active">✅</span>
                                <span v-else>⚪</span>
                            </button>

                            <button v-if="is_staff" @click="goToEdit(form.id)" title="تعديل">✏️</button>
                            <button v-if="is_staff" @click="copyForm(form.id)" title="نسخ">📄</button>
                            <button v-if="is_staff" @click="deleteForm(form.id)" title="حذف">🗑️</button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="card" > لا توجد نماذج للتقديم متاحة الان الرجاء الدخول في وقت لاحق</div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import axios from '@/services/axios';
    import { useRouter } from 'vue-router';

    const forms = ref([]);
    const submissions = ref([]);
    const loading = ref(true);
    const router = useRouter();
    const is_staff = computed(() => {
        const is_staff2 = JSON.parse(localStorage.getItem('user_is_staff'));
        return is_staff2;
    });

    const fetchForms = async () => {
        try {
            const res = await axios.get('api/admissions/forms-list/');
            const res_sub = await axios.get('api/admissions/submissions-list/');
            forms.value = res.data;
            submissions.value = res_sub.data;
        } catch (error) {
            console.error('Error fetching forms:', error);
        } finally {
            loading.value = false;
        }
    };

    const toggleActive = async (form) => {
        try {
            const res = await axios.patch(`api/admissions/forms/${form.id}/`, {
                is_active: !form.is_active,
            });
            form.is_active = res.data.is_active;
        } catch (error) {
            console.error('Error toggling active state:', error);
            alert('حدث خطأ أثناء تعديل حالة النموذج.');
        }
    };

    const goToNew = () => {
        router.push('/admin-form-new');
    };
    const goToNewSubmisson = (id) => {
        router.push(`/submissions/${id}/new`);
    };
    const goToSubmissons = (id) => {
        router.push(`/submissions/${id}/`);
    };

    const goToEdit = (id) => {
        router.push(`/admin-form-edit/${id}`);
    };

    const copyForm = async (id) => {
        const original = forms.value.find((f) => f.id === id);
        if (!original) return;

        const copy = {
            ...original,
            title: `${original.title} (نسخة)`,
        };

        delete copy.id;
        delete copy.submissions_count;
        try {
            const res = await axios.post('api/admissions/forms/', copy);
            await fetchForms();
            alert('تم نسخ النموذج بنجاح');
        } catch (error) {
            console.error('Error copying form:', error);
            alert('حدث خطأ أثناء النسخ');
        }
    };

    const deleteForm = async (id) => {
        if (!confirm('هل أنت متأكد من حذف النموذج؟')) return;
        try {
            await axios.delete(`api/admissions/forms/${id}/`);
            await fetchForms();
        } catch (error) {
            console.error('Error deleting form:', error);
            alert('لا يمكن حذف النموذج، ربما يحتوي على إجابات.');
        }
    };
    const formatDate = (dateStr) => {
        console.log(dateStr);
        if (!dateStr) return '';
        const [datePart, timePart] = dateStr.split(' ');
        const [year, month, day] = datePart.split('-');
        const [hour, minute] = timePart.split(':');
        const date = new Date(year, month - 1, day, hour, minute);

        return date.toLocaleString('ar-EG', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    onMounted(fetchForms);
</script>

<style scoped>
    .btn {
        @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
    }
    button {
        @apply text-blue-600 hover:text-blue-800;
    }
</style>
