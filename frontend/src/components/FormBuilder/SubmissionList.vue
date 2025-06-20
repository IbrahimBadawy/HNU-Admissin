<template>
    <div class="p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">قائمة الطلبات</h2>
            <!-- <button v-if="route.params.formId" class="btn btn-primary" @click="goToNew">➕ طلب جديد</button> -->
        </div>
        <!-- ✅ شريط أدوات البحث والتنقل (للمشرف فقط) -->
        <div v-if="is_staff" class="mb-6 space-y-4">
            <!-- 🔍 شريط البحث -->
            <input v-model="searchTerm" @input="fetchSubmissions" type="text" placeholder="ابحث برقم الطالب أو الطلب..."
                class="w-full px-4 py-2 border rounded shadow-sm" />
            <div class="flex flex-wrap gap-4 items-center">
                <!-- فلتر الحالة -->
                <select v-model="selectedStatus" @change="fetchSubmissions" class="border px-3 py-1 rounded shadow-sm">
                    <option value="">كل الحالات</option>
                    <option value="reviewed">مستوفي</option>
                    <option value="pending">تحت المراجعة</option>
                    <option value="accepted">تم القبول</option>
                    <option value="rejected">تم الرفض</option>
                    <option value="noted">توجد ملاحظات</option>
                </select>

                <!-- فلتر الإغلاق -->
                <select v-model="selectedLock" @change="fetchSubmissions" class="border px-3 py-1 rounded shadow-sm">
                    <option value="">الكل (مفتوح ومغلق)</option>
                    <option :value="true">🔒 مغلق</option>
                    <option :value="false">✅ مفتوح</option>
                </select>
                <!-- فلتر الدفع -->
                <select v-model="selectedPaid" @change="fetchSubmissions" class="border px-3 py-1 rounded shadow-sm">
                    <option value="">الكل (مدفوع وغير مدفوع)</option>
                    <option :value="true">💰 مدفوع</option>
                    <option :value="false">🚫 غير مدفوع</option>
                </select>
                <!-- زر إعادة تعيين الفلاتر -->
                <button @click="resetFilters" class="btn bg-gray-200 text-gray-800 hover:bg-gray-300">
                    🔄 إعادة تعيين الفلاتر
                </button>
                <div class="flex flex-wrap gap-4 items-center mb-4">
                    <div v-for="(qa, index) in qaFilters" :key="index" class="flex gap-2 items-center">
                        <!-- حقل السؤال -->
                        <select v-model="qa.question" @change="qa.answer = ''; fetchSubmissions()"
                            class="border px-3 py-1 rounded shadow-sm">
                            <option value="">-- اختر سؤال --</option>
                            <option v-for="q in uniqueQA" :key="q.question_title" :value="q.question_title">
                                {{ q.question_title }}
                            </option>
                        </select>

                        <!-- حقل الإجابة -->
                        <div class="flex items-center gap-1">
                            <template v-if="qa.editingAnswer">
                                <input type="text" v-model="qa.answer" class="border px-3 py-1 rounded shadow-sm"
                                    placeholder="أدخل نص الإجابة" />
                                <button @click="confirmManualAnswer(qa)"
                                    class="text-green-600 hover:text-green-800 text-lg">✔️</button>
                            </template>
                            <template v-else>
                                <select v-if="qa.question" v-model="qa.answer" @change="fetchSubmissions()"
                                    class="border px-3 py-1 rounded shadow-sm">
                                    <option value="">-- اختر إجابة --</option>
                                    <option
                                        v-for="a in (uniqueQA.find(x => x.question_title === qa.question)?.answers || [])"
                                        :key="a" :value="a">
                                        {{ a }}
                                    </option>
                                </select>
                                <button v-if="qa.question" @click="qa.editingAnswer = true"
                                    class="text-sm text-blue-600 hover:underline">➕ اضف اختيار</button>
                            </template>
                        </div>

                        <!-- زر حذف الفلتر -->
                        <button v-if="qaFilters.length > 1" @click="qaFilters.splice(index, 1); fetchSubmissions()"
                            class="text-red-500 hover:text-red-700 text-lg">&times;</button>
                    </div>

                    <button class="btn mt-2" @click="addQAFilter">➕ إضافة فلتر سؤال</button>
                </div>




            </div>

            <!-- ✅ Pagination ديناميكي -->
            <div v-if="totalPages > 1" class="mt-6 flex flex-wrap justify-center gap-2 items-center text-sm">
                <button class="btn" :disabled="currentPage == 1" @click="currentPage = 1; fetchSubmissions();">
                    الأولى
                </button>
                <!-- السابق -->
                <button class="btn" :disabled="currentPage <= 1" @click="currentPage--; fetchSubmissions();">
                    ⬅️ السابق
                </button>

                <!-- الصفحات -->
                <button v-for="page in paginationPages" :key="page" class="px-3 py-1 rounded border"
                    :class="page === currentPage ? 'bg-blue-600 text-white' : 'bg-white'"
                    @click="currentPage = page; fetchSubmissions();">
                    {{ page }}
                </button>

                <!-- التالي -->
                <button class="btn" :disabled="currentPage >= totalPages" @click="currentPage++; fetchSubmissions();">
                    التالي ➡️
                </button>

                <!-- الأخيرة -->
                <button class="btn" v-if="currentPage < totalPages"
                    @click="currentPage = totalPages; fetchSubmissions();">
                    الأخيرة
                </button>
            </div>

        </div>

        <div v-if="is_staff && totalCount > 0" class="text-sm text-gray-500 mb-2">
            عرض من {{ (currentPage - 1) * 20 + 1 }}
            إلى {{ Math.min(currentPage * 20, totalCount) }}
            من إجمالي {{ totalCount }} سجل
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
                                    <option value="reviewed">مستوفي</option>
                                    <option value="pending">تحت المراجعة</option>
                                    <option value="accepted">تم القبول</option>
                                    <option value="rejected">تم الرفض</option>
                                    <option value="noted">توجد ملاحظات</option>
                                </select>

                                <!-- ✅ ملاحظات -->

                                <button v-if="is_staff" @click="openNoteModal(submission)"
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
                        <button v-if="is_staff || (!is_staff && !submission.is_locked)"
                            @click="set_user_password(submission.user_identifier)"
                            title="استعادة كلمة المرور">🔑</button>

                        <button v-if="is_superadmin" @click="deleteSubmission(submission.id)" title="حذف">🗑️</button>
                    </div>
                </div>
                <!-- ✅ عرض الملاحظة لو موجودة -->
                <div v-if="submission.notes"
                    class="w-full mt-2 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-900 p-3 text-sm rounded">
                    📝 <span class="font-semibold">ملاحظة:</span> {{ submission.notes }}
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
                        <Button type="button" label="الغاء" severity="secondary" @click="visible = false"></Button>
                        <Button type="button" label="حفظ" @click="saveNote"></Button>
                    </div>
                </Dialog>
            </div>
        </div>


    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/services/axios';
const uniqueQA = ref([])
const qaFilters = ref([{ question: '', answer: '' }])

const currentPage = ref(1)
const searchTerm = ref('')
const selectedStatus = ref('')
const selectedLock = ref('')
const selectedPaid = ref('')


const totalPages = ref(1)
const totalCount = ref(0)
const paginationPages = computed(() => {
    const pages = []
    const maxVisible = 5
    const start = Math.max(1, currentPage.value - 2)
    const end = Math.min(totalPages.value, start + maxVisible - 1)

    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

const fetchUniqueQuestionsAndAnswers = async () => {
    try {
        const res = await axios.get(`/api/admissions/forms/${route.params.formId}/unique-questions-answers/`)
        uniqueQA.value = res.data.map(qa => ({
            ...qa,
            editing: false // وضع تحرير افتراضي
        }))
    } catch (error) {
        console.error('Error fetching unique Q&A:', error)
    }
}
const confirmManualAnswer = (qa) => {
    qa.editingAnswer = false;

    if (!qa.question || !qa.answer) return;

    const question = uniqueQA.value.find(x => x.question_title === qa.question);
    if (question && !question.answers.includes(qa.answer)) {
        question.answers.push(qa.answer); // أضفها مؤقتًا إلى القائمة
    }

    fetchSubmissions();
};

const addQAFilter = () => {
    qaFilters.value.push({ question: '', answer: '' })
}
const router = useRouter();
const route = useRoute();
const submissions = ref([]);
const forms = ref([]);
const loading = ref(true);
const showNoteModal = ref(false);
const noteContent = ref('');
const selectedSubmission = ref(null);
const visible = ref(false);
const resetFilters = () => {
    searchTerm.value = ''
    selectedStatus.value = ''
    selectedLock.value = ''
    selectedPaid.value = ''
    qaFilters.value = []
    currentPage.value = 1
    fetchSubmissions()
}
const STORAGE_KEY = 'submissions_filters'


const openNoteModal = (submission) => {
    selectedSubmission.value = submission;
    noteContent.value = submission.notes || '';
    showNoteModal.value = true;
    visible.value = true;
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
const set_user_password = async (user_identifier) => {
    if (!user_identifier) return;
    try {
        const res = await axios.post(`api/users/set_user_password/`, {
            username: user_identifier,
            password: user_identifier,
        });

        // console.log(res.data) 🗝️
        const success = res.data.success
        if (success) { alert("تم استعادة كلمة المرور بنجاح"); }
        const error = res.data.error
        if (error) { alert('فشل تغيير كلمة المرور'); }
    } catch (err) {
        console.error(err)
        alert('فشل تغيير كلمة المرور');
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
            reviewed: 'مستوفي',
            noted: 'توجد ملاحظات',
        }[status] || 'غير معروف'
    );
};

const is_staff = computed(() => {
    const is_staff2 = JSON.parse(localStorage.getItem('user_is_staff'));
    return is_staff2;
});
const is_superadmin = computed(() => {
    const is_superadmin = localStorage.getItem('user_username') === 'ibrahim';
    return is_superadmin;
});


const fetchSubmissions = async () => {
    loading.value = true
    try {
        const params = {
            page: currentPage.value,
            search: is_staff.value ? searchTerm.value : undefined,
            form: route.params.formId || undefined,
            status: selectedStatus.value || undefined,
            is_locked: selectedLock.value !== '' ? selectedLock.value : undefined,
            is_paied: selectedPaid.value !== '' ? selectedPaid.value : undefined,



        }
        // ✅ أضف كل فلتر سؤال/إجابة كـ params
        qaFilters.value.forEach((qa, index) => {
            if (index === 0) {
                if (qa.question) params['question_title'] = qa.question
                if (qa.answer) params['answer_text'] = qa.answer
            } else {
                if (qa.question) params[`question_title_${index}`] = qa.question
                if (qa.answer) params[`answer_text_${index}`] = qa.answer
            }
        })
        const res = await axios.get(`api/admissions/submissions-list/`, { params })

        submissions.value = res.data.results
        totalCount.value = res.data.count
        totalPages.value = Math.ceil(res.data.count / 20)
    } catch (error) {
        console.error('Error loading submissions:', error)
    } finally {
        loading.value = false
    }
}


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

onMounted(() => {
    fetchUniqueQuestionsAndAnswers()
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')

    searchTerm.value = saved.searchTerm || ''
    selectedStatus.value = saved.selectedStatus || ''
    selectedLock.value = saved.selectedLock ?? ''
    selectedPaid.value = saved.selectedPaid ?? ''
    qaFilters.value = saved.qaFilters ?? []
    currentPage.value = saved.currentPage || 1

    fetchSubmissions()

})

watch(
    [searchTerm, selectedStatus, selectedLock, selectedPaid, qaFilters, currentPage],
    () => {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
                searchTerm: searchTerm.value,
                selectedStatus: selectedStatus.value,
                selectedLock: selectedLock.value,
                selectedPaid: selectedPaid.value,
                qaFilters: qaFilters.value,
                currentPage: currentPage.value,
            })
        )
    },
    { deep: true }
)

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

.status-reviewed {
    @apply bg-green-100 text-green-800 px-2 py-1 rounded;
}

.status-noted {
    @apply bg-yellow-100 text-yellow-800 px-2 py-1 rounded;
}

.status-noted {
    @apply bg-yellow-100 text-yellow-800 px-2 py-1 rounded;
}
.status-noted {
    @apply bg-yellow-100 text-yellow-800 px-2 py-1 rounded;
}
.status-noted {
    @apply bg-yellow-100 text-yellow-800 px-2 py-1 rounded;
}
</style>
