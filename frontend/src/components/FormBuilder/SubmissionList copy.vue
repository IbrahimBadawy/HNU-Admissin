<template>
    <div class="p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">قائمة الطلبات</h2>
            <button v-if="route.params.formId" class="btn btn-primary" @click="goToNew">➕ طلب جديد</button>
        </div>

        <div v-if="loading" class="text-gray-500">جاري التحميل...</div>

        <div v-else class="space-y-3">
            <div v-for="submission in submissions" :key="submission.id" class="flex justify-between items-center p-4 bg-white border rounded shadow">
                <div @click="goToView(submission.form, submission.id)">
                    <div class="flex items-center gap-4">
                        <div class="text-lg font-semibold">طلب رقم #{{ submission.id }}</div>
                        <div class="text-lg mr-5 font-semibold">الطالب #{{ ` ${submission.user_identifier}` }}</div>
                        <div class="text-sm text-gray-500">
                            <span class="font-bold bg-blue-100 text-blue-800 px-2 py-1 rounded mr-2"
                                >الحالة {{ submission.is_locked ? 'مغلق' : 'مفتوح' }}
                            </span>
                            <span class="mr-7 text-gray-400">آخر تحديث: {{ formatDate(submission.modified_at) }}</span>
                        </div>
                    </div>
                </div>

                <div class="flex gap-3 text-xl items-center">
                    <button v-if="is_staff" @click="toggleActive(submission)" :title="submission.is_locked ? 'فتح' : 'غلق'">
                        <span v-if="submission.is_locked">🗝️</span>
                        <span v-else>🔒</span>
                    </button>
                    <button @click="goToView(submission.form, submission.id)" title="عرض">👁️</button>

                    <button v-if="is_staff || (!is_staff && !submission.is_locked)" @click="goToEdit(submission.form, submission.id)" title="تعديل">✏️</button>
                    <button v-if="is_staff" @click="deleteSubmission(submission.id)" title="حذف">🗑️</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import axios from '@/services/axios';

    const router = useRouter();
    const route = useRoute();
    const submissions = ref([]);
    const forms = ref([]);
    const loading = ref(true);

    const is_staff = computed(() => {
        const is_staff2 = JSON.parse(localStorage.getItem('user_is_staff'));
        return is_staff2;
    });

    const fetchSubmissions = async () => {
        try {
            const res_forms = await axios.get(`api/admissions/forms/`);
            var res = {};
            forms.value = res_forms.data;
            res = await axios.get(`api/admissions/submissions-list/`);
            var temp = [];
            if (route.params.formId) {
                const formId = Number(route.params.formId);
                for (const submission of res.data) {
                    if (submission.form === formId) {
                        temp.push(submission);
                    }
                }
                submissions.value = temp;
            } else {
                submissions.value = res.data;
            }
        } catch (error) {
            console.error('Error loading submissions:', error);
        } finally {
            loading.value = false;
        }
    };

    const goToNew = () => router.push(`/submissions/${route.params.formId}/new`);
    const goToEdit = (form_id, id) => router.push(`/submissions/${form_id}/${id}/edit`);
    const goToView = (form_id, id) => router.push(`/submissions/${form_id}/${id}`);

    const deleteSubmission = async (id) => {
        if (!confirm('هل أنت متأكد من حذف هذا الطلب؟')) return;
        try {
            await axios.delete(`api/admissions/submissions/${id}/`);
            await fetchSubmissions();
        } catch (error) {
            alert('لا يمكن حذف الطلب.');
        }
    };
    const toggleActive = async (submission) => {
        try {
            const res = await axios.patch(`api/admissions/submissions/${submission.id}/`, {
                is_locked: !submission.is_locked,
            });
            submission.is_locked = res.data.is_locked;
        } catch (error) {
            console.error('Error toggling active state:', error);
            alert('حدث خطأ أثناء تعديل حالة النموذج.');
        }
    };
    const formatDate = (dateStr) => {
        // console.log(dateStr);
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

    onMounted(fetchSubmissions);
</script>

<style scoped>
    .btn {
        @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
    }
</style>
