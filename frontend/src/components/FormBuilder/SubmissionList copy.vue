<template>
    <div class="p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">قائمة الطلبات</h2>
            <!-- <button v-if="route.params.formId" class="btn btn-primary" @click="goToNew">➕ طلب جديد</button> -->
        </div>

        <div v-if="loading" class="text-gray-500">جاري التحميل...</div>
        

        <div v-else class="space-y-3">
            <div v-for="submission in submissions" :key="submission.id" class="p-4 bg-white border rounded shadow ">
                <!-- ✅ معلومات الطلب -->
                <div
                    class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">

                    <div class="w-full md:w-auto">
                        <div class="flex flex-col md:flex-row md:items-center gap-4">
                            <!-- رقم الطلب -->
                            <div @click="goToView(submission.form, submission.id)"
                                class="text-lg font-semibold cursor-pointer">
                                طلب رقم #{{ submission.id }}
                            </div>

                            <!-- رقم الطالب -->
                            <div @click="goToView(submission.form, submission.id)"
                                class="text-lg font-semibold cursor-pointer">
                                الطالب #{{ submission.user_identifier }}
                            </div>

                            <!-- ✅ الحالة -->
                            <div class="flex flex-col md:flex-row md:items-center text-sm text-gray-500 gap-2 md:gap-4">
                                <span class="font-bold bg-yellow-100 text-yellow-800 px-2 py-1 rounded"
                                    :class="'status-' + submission.status">
                                    الحالة: {{ getStatusLabel(submission.status) }}
                                </span>

                                <!-- ✅ إشارة الدفع -->
                                <span v-if="submission.is_paied"
                                    class="font-bold text-green-700 bg-green-100 px-2 py-1 rounded">
                                    💰 تم الدفع
                                </span>

                                <!-- ✅ اختيار الحالة -->
                                <select v-if="is_staff" v-model="submission.status"
                                    class="text-sm px-2 py-1 rounded border" :class="'status-' + submission.status"
                                    @change="updateStatus(submission)">
                                    <option value="pending">تحت المراجعة</option>
                                    <option value="accepted">تم القبول</option>
                                    <option value="rejected">تم الرفض</option>
                                    <option value="noted">توجد ملاحظات</option>
                                </select>

                                <!-- ✅ ملاحظات -->

                                <button v-if="is_staff" @click="visible = true"
                                    class="text-sm px-2 py-1 bg-gray-100 rounded" :class="'status-noted'">
                                    📝 </button>

                                <!-- ✅ آخر تحديث -->
                                <span class="text-xs text-gray-400">
                                    آخر تحديث: {{ formatDate(submission.modified_at) }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- ✅ أزرار الإدارة -->
                    <div class="flex gap-3 text-xl items-center md:justify-end w-full md:w-auto">
                        <button v-if="is_staff" @click="toggleActive(submission)"
                            :title="submission.is_locked ? 'فتح' : 'غلق'">
                            <span v-if="submission.is_locked">🗝️</span>
                            <span v-else>🔒</span>
                        </button>

                        <button @click="goToView(submission.form, submission.id)" title="عرض">👁️</button>

                        <button v-if="is_staff || (!is_staff && !submission.is_locked)"
                            @click="goToEdit(submission.form, submission.id)" title="تعديل">✏️</button>

                        <button v-if="is_staff" @click="deleteSubmission(submission.id)" title="حذف">🗑️</button>
                    </div>
                </div>
                <!-- ✅ عرض الملاحظة لو موجودة -->
                <div v-if="noteContent"
                    class="w-full mt-2 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-900 p-3 text-sm rounded">
                    📝 <span class="font-semibold">ملاحظة:</span> {{ noteContent }}
                </div>

                <!-- ✅ المودال -->

                <Dialog v-model:visible="visible" modal header="اضافة ملاحظة" :style="{ width: '25rem' }">
                    <span class="text-surface-500 dark:text-surface-400 block mb-8">اضف ملاحظة للطلب رقم {{
                        submission.id }}</span>
                    <div class="flex items-center gap-4 mb-4">
                        <label for="note" class="font-semibold w-24">الملاحظة</label>
                        <Textarea v-model="noteContent" rows="5" cols="30" id="note" class="flex-auto"
                            autocomplete="off" />
                    </div>

                    <div class="flex justify-end gap-2">
                        <Button type="button" label="الغاء" severity="secondary" @click="saveNote"></Button>
                        <Button type="button" label="حفظ" @click="visible = false"></Button>
                    </div>
                </Dialog>
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
const showNoteModal = ref(false);
const noteContent = ref('');
const selectedSubmission = ref(null);
const visible = ref(false);

const openNoteModal = (submission) => {
    selectedSubmission.value = submission;
    noteContent.value = submission.notes || '';
    showNoteModal.value = true;
};

const saveNote = async () => {
    if (!selectedSubmission.value) return;
    try {
        await axios.patch(`api/admissions/submissions/${selectedSubmission.value.id}/`, {
            notes: noteContent.value,
        });
        selectedSubmission.value.notes = noteContent.value;
        showNoteModal.value = false;
        visible.value = false
    } catch (err) {
        alert('فشل حفظ الملاحظات');
    }
};

const updateStatus = async (submission) => {
    try {
        await axios.patch(`api/admissions/submissions/${submission.id}/`, {
            status: submission.status,
        });
    } catch (err) {
        alert('حدث خطأ أثناء تحديث الحالة');
    }
};

const getStatusLabel = (status) => {
    return (
        {
            pending: 'تحت المراجعة',
            accepted: 'تم القبول',
            rejected: 'تم الرفض',
            noted: 'توجد ملاحظات',
        }[status] || 'غير معروف'
    );
};

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

.status-pending {
    @apply bg-blue-100 text-blue-800 px-2 py-1 rounded;
}

.status-accepted {
    @apply bg-green-100 text-green-800 px-2 py-1 rounded;
}

.status-rejected {
    @apply bg-red-100 text-red-800 px-2 py-1 rounded;
}

.status-noted {
    @apply bg-yellow-100 text-yellow-800 px-2 py-1 rounded;
}
</style>
