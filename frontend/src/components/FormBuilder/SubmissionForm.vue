<template>
    <div class="p-4 space-y-6">
        <form-wizard v-if="form" shape="circle" color="#4361ee" class="circle" @on-complete=""
            :start-index="route.params.tabId - 1 || 0" step-size="xs" nextButtonText="التالي" backButtonText="السابق"
            finishButtonText="انهاء">
            <tab-content v-for="tab in form.tabs" :key="tab.id" :title="tab.title" :before-change="() => nextTab(tab)">
                <div v-for="section in tab.sections" :key="section.id" class="mb-4">
                    <div v-if="section.meta_data.is_visible">
                        <h3 class="text-lg font-semibold mb-2 text-center sm:text-right">
                            {{ section.title }}
                        </h3>

                        <div v-for="question in section.questions" :key="question.id"
                            class="border p-4 rounded shadow mb-4 flex flex-col gap-2">
                            <h4 class="font-semibold">{{ question.title }}</h4>

                            <QuestionRenderer :type="question.question_type" :mode="mode" :question="question"
                                v-model="answers[question.id]" :configs="question.configs || {}"
                                :options="question.options || []" v-model:errorState="errors[question.id]" />
                        </div>
                    </div>
                </div>
            </tab-content>
        </form-wizard>
        <div v-if="submission_dat.notes"
            class="w-full mt-2 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-900 p-3 text-sm rounded">
            📝 <span class="font-semibold">ملاحظة:</span> {{ submission_dat.notes }}
        </div>
        <!-- ✅ أزرار الإرسال -->
        <div v-if="submission_dat"
            class="mt-6 flex flex-col sm:flex-row w-full justify-center items-center sm:items-start gap-4">
            <button v-if="is_staff" class="btn w-full sm:w-auto" @click="toggleActive(submission_dat)"
                :title="submission_dat.is_locked ? 'فتح النموذج للطالب' : 'غلق النموذج للطالب'">
                <span v-if="submission_dat.is_locked">فتح</span>
                <span v-else>غلق</span>
            </button>

            <div v-if="mode === 'view' && !is_staff && !submission_dat.is_locked" class="w-full sm:w-auto">
                <button class="btn w-full sm:w-auto" @click="goToEdit(formId, submissionId, route.params.tabId || 1)">
                    تعديل ✏️
                </button>
            </div>
            <div v-if="mode === 'view' && is_superadmin && !submission_dat.is_locked" class="w-full sm:w-auto">
                <button class="btn w-full sm:w-auto" @click="goToEdit(formId, submissionId, route.params.tabId || 1)">
                    تعديل ✏️
                </button>
            </div>

            <!-- ✅ ملاحظات -->

            <button v-if="is_staff" @click="openNoteModal()" class="text-sm px-2 py-1 bg-gray-100 rounded"
                :class="'status-noted'">
                📝 </button>
            <span class="font-bold bg-yellow-100 text-yellow-800 px-2 py-1 rounded"
                :class="'status-' + submission_dat.status">
                الحالة: {{ getStatusLabel(submission_dat.status) }}
            </span>

            <!-- ✅ اختيار الحالة -->
            <select v-if="is_staff" v-model="submission_dat.status" class="text-sm px-2 py-1 rounded border"
                :class="'status-' + submission_dat.status" @change="updateStatus(submission_dat)">
                <option value="reviewed">مستوفي</option>
                <option value="pending">تحت المراجعة</option>
                <option value="accepted">تم القبول</option>
                <option value="rejected">تم الرفض</option>
                <option value="noted">توجد ملاحظات</option>
            </select>

            <div v-if="mode === 'edit' && !route.path.includes('new')" class="w-full sm:w-auto">
                <button class="btn w-full sm:w-auto" @click="goToSave(formId, submissionId, route.params.tabId || 1)">
                    حفظ
                </button>
            </div>

            <div class="w-full sm:w-auto">
                <button class="btn w-full sm:w-auto" @click="goToBack(formId)">
                    عودة
                </button>
            </div>

        </div>

        <div v-if="is_staff" class="my-4 ">
            <label class="block font-bold mb-2">ترشيح لبرنامج</label>
            <select v-model="submission_dat.program" class="form-select" @change="saveProgram">
                <option value="">بدون ترشيح</option>
                <optgroup v-for="f in groupedPrograms" :key="f.id" :label="f.name">
                    <option v-for="p in f.programs" :value="p.id" :key="p.id">
                        {{ p.sis_code }} - {{ p.name }}
                    </option>
                </optgroup>
            </select>
        </div>
        <div v-if="submission_dat.program">
            <div class="bg-green-100 text-green-800 p-2 rounded">
                مرشح للبرنامج:
                {{ getProgramName(submission_dat.program) }}
            </div>
            <button class="btn mt-2" @click="openFeesModal">دفع مصاريف الكلية</button>

        </div>
        <!-- ✅ المودال -->
        <Dialog v-model:visible="showFeesModal" modal header="دفع مصاريف الكلية" :style="{ width: '40rem' }">
            <div v-if="availableFees.length">

                <!-- ✅ المصاريف المتاحة للاختيار -->
                <p>اختر المصاريف التي تريد دفعها:</p>
                <div v-for="f in availableFees" :key="'available-' + f.id" class="flex items-center gap-2 my-2">
                    <input type="checkbox" :value="f.id" v-model="selectedFeeIds" :disabled="f.is_requierd" checked />
                    <span>
                        {{ f.description }} - {{ f.amount }} EGP - {{ f.fee_list_title }}
                        <span v-if="f.is_requierd" class="text-red-600">(إجباري)</span>
                    </span>
                </div>

                <div class="mt-4 border-t pt-2 text-right">
                    <p>المجموع بدون عمولة: <strong>{{ totalSelectedAmount.total }} جنيه</strong></p>
                    <p>عمولة البنك: <strong>{{ totalSelectedAmount.bankFee }} جنيه</strong></p>
                    <p class="text-lg mt-1">
                        الإجمالي المطلوب: <strong class="text-green-700">{{ totalSelectedAmount.finalTotal }}
                            جنيه</strong>
                    </p>
                </div>
            </div>
            <div v-else>
                <p>لا توجد رسوم للدفع</p>
            </div>

            <!-- ✅ المصاريف المدفوعة للعرض فقط -->
            <div v-if="paidFees.length" class="mt-4 border-t pt-4">
                <p class="text-gray-700 font-semibold mb-2">المصاريف التي تم دفعها:</p>
                <div v-for="f in paidFees" :key="'paid-' + f.id" class="flex items-center gap-2 my-1 text-gray-500">
                    <input type="checkbox" checked disabled />
                    <span>{{ f.description }} - {{ f.amount }} EGP</span>
                </div>
            </div>



            <div class="flex justify-end mt-4 gap-2">
                <Button label="إلغاء" severity="secondary" @click="showFeesModal = false" />
                <Button v-if="availableFees.length" label="دفع" @click="paySelectedFees" />
            </div>
        </Dialog>


        <Dialog v-model:visible="visible" modal header="اضافة ملاحظة" :style="{ width: '25rem' }">
            <span class="text-surface-500 dark:text-surface-400 block mb-8">اضف ملاحظة للطلب رقم {{
                submission_dat.id }}</span>
            <div class="flex items-center gap-4 mb-4">
                <label for="note" class="font-semibold w-24">الملاحظة</label>
                <Textarea v-model="noteContent" rows="5" cols="30" id="note" class="flex-auto" autocomplete="off" />
            </div>

            <div class="flex justify-end gap-2">
                <Button type="button" label="الغاء" severity="secondary" @click="visible = false"></Button>
                <Button type="button" label="حفظ" @click="saveNote"></Button>
            </div>
        </Dialog>
    </div>

</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/services/axios';
import QuestionRenderer from '@/components/QuestionRenderer/QuestionRenderer.vue';
import { validateValue } from '@/components/QuestionRenderer/utils/validation';

import Swal from 'sweetalert2';
import { FormWizard, TabContent } from 'vue3-form-wizard';
import 'vue3-form-wizard/dist/style.css';
import { cloneElement } from '@fullcalendar/core/preact';

const is_staff = computed(() => {
    const is_staff2 = JSON.parse(localStorage.getItem('user_is_staff'));
    return is_staff2;
});

const route = useRoute();
const router = useRouter();
const mode = ref('view');

const qRefs = reactive({});
const nowSections = ref({});

const form = ref(null);
const submission_dat = ref({
    id: 0,
    notes: "",
    status: "",
    program: "",
    is_archived: false,
    meta_data: {},
    answers: [],
    modified_at: '2025-05-05 07:06',
    user_identifier: 'ibrahim',
    is_locked: false,
    submitted_at: '2025-05-05T07:06:56.321830+03:00',
    form: 20,
});
const is_locked = ref(false);
const answers = reactive({});
const questions = reactive({});
const errors = reactive({});

const submissionId = ref('');
const formId = ref('');

const hasErrors = computed(() => Object.values(errors).includes(true));
const showNoteModal = ref(false);
const noteContent = ref('');
const selectedSubmission = ref(null);
const visible = ref(false);


const faculties = ref([]);
const groupedPrograms = ref([]);

const fetchProgramsAndFaculties = async () => {
    const resFac = await axios.get('/api/users/faculties/');
    const resProg = await axios.get('/api/users/programs/');
    const facs = resFac.data.results || resFac.data;
    const progs = resProg.data.results || resProg.data;
console.log(facs)
    groupedPrograms.value = facs.map(fac => {
        const facProgs = progs
            .filter(p => p.faculty === fac.id || p.faculty?.id === fac.id)
            .sort((a, b) => (a.sis_code || '').localeCompare(b.sis_code || ''));

        const firstSisCode = facProgs.length ? (facProgs[0].sis_code || '') : '';
        return {
            id: fac.id,
            name: fac.name,
            firstSisCode,
            programs: facProgs,
        };
    }).filter(f => f.programs.length > 0)
        .sort((a, b) => a.firstSisCode.localeCompare(b.firstSisCode));
};

const showFeesModal = ref(false);
const availableFees = ref([]);
const selectedFeeIds = ref([]);
const paidFees = ref([]);
const availablePaiedFees = ref([]);
const feesTypes = ref([]);
const feesLists = ref([]);
function getSelectedFeeTypeId(val) {
    const type = feesTypes.value.find(t => t.value === val);
    return type ? type.id : '';
}
function filterProgramFeesByType(typeValue, programFees, feesLists, feesTypes) {
    // console.log("#############")
    // console.log(typeValue)
    // console.log(programFees)
    // console.log(feesLists)
    // console.log(feesTypes)
    // console.log("#############")
    if (!typeValue || !feesTypes.length || !feesLists.length || !programFees.length) return [];
    // 1. نحصل على ID من feesTypes بناءً على الـ value
    const type = feesTypes.find(t => t.value === typeValue);
    if (!type) return [];

    const typeId = type.id;

    // 2. نحصل على IDs للـ fee lists اللي تنتمي لنوع المصروف المطلوب
    const matchingFeeListIds = feesLists
        .filter(feeList => feeList.fees_types?.id === typeId)
        .map(feeList => feeList.id);

    // 3. نفلتر programFees اللي fee_list فيها موجود ضمن الـ matching IDs
    return programFees.filter(fee => matchingFeeListIds.includes(fee.fee_list));
}
const openFeesModal = async () => {
    const res = await axios.get('/api/payments/program-fees/', {
        params: {
            academic_year: form.value.academic_year,
            program: submission_dat.value.program,
        }
    });
    var programFees = res.data.results || res.data;
    const feesTypesRes = await axios.get('/api/payments/fees-types/')
    feesTypes.value = feesTypesRes.data.results || feesTypesRes.data;
    const feesListsRes = await axios.get('/api/payments/fees-list/')
    feesLists.value = feesListsRes.data.results || feesListsRes.data;


    programFees = programFees.map(fee => {
        const matchedList = feesLists.value.find(f => f.id === fee.fee_list);
        return {
            ...fee,
            fee_list_title: matchedList ? matchedList.title : '',
        };
    });


    const paidFeesRes = await axios.get('/api/payments/fees/', {
        params: { submission_id: submission_dat.value.id }
    });
    paidFees.value = paidFeesRes.data.results.filter(f => f.is_paid && f.fee_type == 'collage');


    // استخراج الرسوم المتاحة (فقط مصاريف الكلية وغير مدفوعة)
    availableFees.value = filterProgramFeesByType('collage', programFees, feesLists.value, feesTypes.value);
    // availablePaiedFees.value = filterProgramFeesByType('collage', paidFees, feesLists.value, feesTypes.value);


    const paidFeesListIds = paidFees.value.map(f => f.fees_list); // استخرج الـ fee_list من كل مدفوع

    const filteredAvailableFees = availableFees.value.filter(fee =>
        !paidFeesListIds.includes(fee.id)  // قارن مع الـ available fee.id لأنه يمثل نفس الـ fees_list
    );

    availableFees.value = filteredAvailableFees;

    // console.log("availableFees")
    // console.log("############")
    // console.log(paidFees.value)
    // console.log(availableFees.value)
    // console.log("############")
    selectedFeeIds.value = availableFees.value
        .map(f => f.id);

    showFeesModal.value = true;
};

const paySelectedFees = async () => {
    if (!selectedFeeIds.value.length) return alert("اختر رسوم للدفع");

    const feeResList = [];
    let totalAmount = 0;

    for (let feeId of selectedFeeIds.value) {
        const feeObj = availableFees.value.find(f => f.id === feeId);
        if (!feeObj) continue;
        try {
            // أضف رسوم إلى الطلب (fee object)
            const feeRes = await axios.post('/api/payments/fees/add-to-submission/', {
                submission_id: Number(submission_dat.value.id),
                description: feeObj.fee_list_title,
                amount: feeObj.amount,
                fee_list_id: feeObj.id,
                fee_type: 'collage',
            });

            // إجمع المبلغ الكلي
            totalAmount += feeObj.amount;
            feeResList.push(feeRes.data.id); // ← لازم تاخد ID من السيرفر
        } catch (error) {
            // console.error(`فشل إرسال الرسوم (${fee.description}):`, error);
            // يمكنك أيضًا استخدام showToast أو أي إشعار للتنبيه
        }
    }

    if (!feeResList.length) return alert("لم يتم إنشاء رسوم بنجاح");

    // إنشاء الطلب والدفع
    const payRes = await axios.post('/api/payments/initiate/', {
        fee_ids: feeResList,
        form_id: form.value.id,
        submission_id: submission_dat.value.id,
        order_type: 'collage',
    });
    localStorage.setItem('pending_payment_order', payRes.data.order_id);

    window.location.href = payRes.data.redirect_url;
};


const getProgramName = (id) => {

    for (let f of groupedPrograms.value) {
        const p = f.programs.find(prog => prog.id === id);
        if (p) return p.name;
    }
    return '';
};

const openNoteModal = () => {
    noteContent.value = submission_dat.value.notes || '';
    showNoteModal.value = true;
    visible.value = true;
};

const saveNote = async () => {
    if (!submission_dat.value) return;
    try {
        await axios.patch(`api/admissions/submissions/${submission_dat.value.id}/`, {
            notes: noteContent.value,
        });
        submission_dat.value.notes = noteContent.value;
        showNoteModal.value = false;
        visible.value = false
    } catch (err) {

        alert('فشل حفظ الملاحظات');
    }
};
const saveProgram = async () => {
    try {
        await axios.patch(`api/admissions/submissions/${submission_dat.value.id}/`, {
            program: submission_dat.value.program,
        });
    } catch (err) {

        alert('فشل حفظ البرنامج');
    }
};

const checkQuestionsn = (tab) => {
    const anss = answers;
    let result = true; // ✅ يبدأ بـ true
    let allErrors = []; // ✅ يبدأ بـ true

    for (const section of tab.sections) {
        if (section.meta_data.is_visible) {
            for (const question of section.questions) {
                const rules = question.configs.rules || [];
                if (rules.length > 0) {
                    const q_type = question.question_type;
                    const ans = anss[question.id];

                    const error = !!validateValue(ans, rules, q_type);
                    // console.log(`q_type : ${q_type} role: ${JSON.stringify(error, null, 2)} ans: ${ans} error : ${error}`);
                    allErrors.push(error);
                }
            }
        }
    }
    result = allErrors.includes(true);

    // console.log(JSON.stringify(result, null, 2));
    return result;
};

const totalSelectedAmount = computed(() => {
    const selectedFees = availableFees.value.filter(f => selectedFeeIds.value.includes(f.id));
    const total = selectedFees.reduce((sum, f) => sum + parseFloat(f.amount || 0), 0);
    const bankFee = Math.round((total * 0.01 + 2) * 100) / 100;
    return {
        total,
        bankFee,
        finalTotal: Math.round((total + bankFee) * 100) / 100,
    };
});
const checkOptions = (index) => {
    const anss = answers;
    const tab = form.value.tabs[index];
    // console.log(index);
    if (index < form.value.tabs.length) {
        for (const section of tab.sections) {
            if (section.meta_data.is_visible) {
                for (const question of section.questions) {
                    if (question.options.length > 0) {
                        const newOptions = [];

                        // console.log(JSON.stringify(question, null, 2))

                        const related_question_title = question.meta_data.depend_question.name;
                        const related_question = findQuestionByTitleValue(form.value.tabs, related_question_title);
                        // console.log(related_question_title)
                        if (!related_question) continue; // skip this question if dependency is not found

                        const related_question_id = related_question.question.id;

                        const ans = anss[related_question_id];

                        for (const option of question.options) {
                            const rules = option.meta_data.rules || [];
                            // console.log(rules)
                            if (Array.isArray(rules) && rules.length > 0) {
                                const q_type = option.meta_data.type_of_rules;

                                const error = validateValue(ans, rules, q_type);
                                // console.log(JSON.stringify(ans, null, 2));
                                // console.log(JSON.stringify(rules, null, 2));
                                // console.log(JSON.stringify(q_type, null, 2));
                                // console.log(JSON.stringify(validateValue(ans, rules, q_type), null, 2));
                                if (error) {
                                    option.meta_data.is_locked = true;
                                } else {
                                    option.meta_data.is_locked = false;
                                }
                            } else {
                                option.meta_data.is_locked = false;
                            }
                            // console.log(option.meta_data.is_locked);
                        }
                        // question.options = (newOptions);
                    }
                }
            }
        }
    }
    return tab;
};

const nextTab = (tab) => {
    const count_tabs = form.value.tabs.length;
    const check = tab.order < count_tabs;
    var error = false
    if (check) {

        error = checkQuestionsn(tab);
    }
    // console.log(tab.order);
    const atab = checkOptions(tab.order);
    if (!error) {

        // console.log(`check : ${check}`);
        submit(check, tab.order + 1, 'next');
        return true;
    } else {
        alert('يرجى ملء جميع الحقول المطلوبة');
        return false;
    }
};

function updateSectionVisibility() {
    if (!form.value || !Array.isArray(form.value.tabs)) return;

    form.value.tabs.forEach((tab) => {
        const dependMeta = tab.meta_data?.depend_question;
        let triggerAnswer = null;

        if (dependMeta?.name) {
            const find_data = findQuestionByTitleValue(form.value.tabs, dependMeta.name);
            if (find_data) {
                triggerAnswer = answers[find_data.question.id];
            }
        }

        tab.sections.forEach((section) => {
            if (!section.meta_data) section.meta_data = {};
            let res = false;

            try {
                // ✅ لو مفيش شرط، نخليها ظاهرة دائمًا
                if (!dependMeta?.name) {
                    res = true;
                } else if (Array.isArray(triggerAnswer)) {
                    res = triggerAnswer.includes(section.title);
                } else if (typeof triggerAnswer === 'string' && triggerAnswer.startsWith('[')) {
                    const parsed = JSON.parse(triggerAnswer);
                    res = Array.isArray(parsed) && parsed.includes(section.title);
                } else {
                    res = String(triggerAnswer) === String(section.title);
                }
            } catch (err) {
                res = false;
            }

            section.meta_data.is_visible = res;
        });
    });
    // console.log("قققققق")
    const filteredAnswers = {};
    const filteredQuestions = {};

    for (const [id, answer] of Object.entries(answers)) {
        if (answer !== null && answer !== '' && answer !== undefined) {
            filteredAnswers[id] = answer;
            filteredQuestions[id] = questions[id];  // خزن السؤال اللي إجابته موجودة فقط
        }
    }

    localStorage.setItem('answers', JSON.stringify(filteredAnswers));
    localStorage.setItem('questions', JSON.stringify(filteredQuestions));


    // console.log(JSON.stringify(form.value, null, 2));
}
watch(answers, updateSectionVisibility, { deep: true });

const fetchForm = async () => {
    submissionId.value = route.params.id || '';
    formId.value = route.params.formId || '';
    if (route.path.includes('edit') || route.path.includes('new')) {
        mode.value = 'edit';
    }
    try {
        const res = await axios.get(`api/admissions/forms/${formId.value}/`);
        form.value = res.data;

        // جهز الحقول
        form.value.tabs.forEach((tab) => {
            tab.sections.forEach((section) => {
                section.questions.forEach((q) => {
                    questions[q.id] = q.title;
                    answers[q.id] = '';
                    errors[q.id] = false;
                });
            });
        });

        // لو تعديل أو عرض، هات البيانات
        if (submissionId.value) {
            const res2 = await axios.get(`api/admissions/submissions/${submissionId.value}/`);
            submission_dat.value = res2.data;
            localStorage.setItem(`submission_dat`, JSON.stringify(res2.data));

            is_locked.value = submission_dat.value.is_locked;
            submission_dat.value.answers.forEach((ans) => {
                if (answers.hasOwnProperty(ans.question)) {
                    answers[ans.question] = ans.answer_text;
                }
            });
        }

        if (form.value.meta_data.start_index) {
            if (!route.params.tabId) {
                if (mode.value === 'edit') {
                    router.push(`/submissions/${formId.value}/${submissionId.value}/edit/${form.value.meta_data.start_index + 1}`);
                } else {
                    router.push(`/submissions/${formId.value}/${submissionId.value}/${form.value.meta_data.start_index + 1}`);
                }
            }
        }
    } catch (err) {
        console.error('Error loading form/submission:', err);
    }
};
const is_superadmin = computed(() => {
    const is_superadmin = localStorage.getItem('user_username') === 'ibrahim';
    return is_superadmin;
});
const submit = async (check = false, index, source) => {
    // في الدالة submit:
    if (mode.value === 'edit') {
        const payload = {
            form: form.value.id,
            answers: Object.entries(answers).map(([question, answer_text]) => ({
                question,
                answer_text: Array.isArray(answer_text) ? JSON.stringify(answer_text) : answer_text,
            })),
        };

        // console.log(index);

        try {
            if (index != 2) {
                await axios.put(`api/admissions/submissions/${submissionId.value}/`, payload);
                if (check) {
                    router.push(`/submissions/${formId.value}/${submissionId.value}/edit/${index}`);
                } else {
                    router.push(`/submissions/${formId.value}/`);
                }
            } else {
                if (route.path.includes('new')) {
                    const res = await axios.post('api/admissions/submissions/', payload);
                    formId.value = res.data.form;
                    submissionId.value = res.data.id;
                    router.push(`/submissions/${formId.value}/${submissionId.value}/edit/2`);

                } else {
                    await axios.put(`api/admissions/submissions/${submissionId.value}/`, payload);
                    router.push(`/submissions/${route.params.formId}/${route.params.id}/edit/${route.params.tabId + 1}`);
                }
            }


            form.value.meta_data.start_index = index - 2;
        } catch (err) {
            alert('فشل في إرسال النموذج');
            console.error(err);
        }
    } else {
        if (check) {
            router.push(`/submissions/${formId.value}/${submissionId.value}/${index}`);
        } else {
            router.push(`/submissions/${formId.value}/`);
        }
    }
};
const toggleActive = async (submission) => {
    try {
        const res = await axios.patch(`api/admissions/submissions/${submission.id}/`, {
            is_locked: !submission.is_locked,
        });
        submission_dat.value.is_locked = res.data.is_locked;
    } catch (error) {
        console.error('Error toggling active state:', error);
        alert('حدث خطأ أثناء تعديل حالة النموذج.');
    }
};

const goToBack = (id) => router.push(`/submissions/${id}`);
const goToEdit = (f_id, s_id, t_id) => {
    router.push(`/submissions/${f_id}/${s_id}/edit/${t_id}`);
    mode.value = 'edit';
};
const goToSave = async (f_id, s_id, t_id) => {
    const payload = {
        form: form.value.id,
        answers: Object.entries(answers).map(([question, answer_text]) => ({
            question,
            answer_text: Array.isArray(answer_text) ? JSON.stringify(answer_text) : answer_text,
        })),
    };

    await axios.put(`api/admissions/submissions/${s_id}/`, payload);
    // router.push(`/submissions/${f_id}/${s_id}/${t_id}`);
    mode.value = 'view';
};
onMounted(async () => {
    await fetchForm();
    updateSectionVisibility();
    fetchProgramsAndFaculties();
});
function extractTitlesFromTabs(tabs) {
    const result = [];

    if (!Array.isArray(tabs)) return result;

    tabs.forEach((tab) => {
        if (!tab.sections) return;

        tab.sections.forEach((section) => {
            if (!section.questions) return;

            section.questions.forEach((question) => {
                const dat = `${tab.title} | ${section.title} | ${question.title}`;
                result.push({ name: dat, code: dat });
            });
        });
    });

    return result;
}

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

function findQuestionByTitleValue(tabs, value) {
    if (!Array.isArray(tabs) || typeof value !== 'string') return null;

    const [tabTitle, sectionTitle, questionTitle] = value.split('|').map((s) => s.trim());

    for (const tab of tabs) {
        if (tab.title !== tabTitle) continue;

        for (const section of tab.sections || []) {
            if (section.title !== sectionTitle) continue;

            for (const question of section.questions || []) {
                if (question.title === questionTitle) {
                    return {
                        tab,
                        section,
                        question,
                    };
                }
            }
        }
    }

    return null;
}
</script>

<style scoped>
.btn {
    padding: 10px 20px;
    background: #2c7be5;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    transition: 0.3s;
}

.btn.bg-gray-500 {
    background: #6b7280;
}
</style>

<style>
.vue-form-wizard .wizard-progress-bar {
    float: right !important;
}

.vue-form-wizard .wizard-card-footer {
    display: flex !important;
    justify-content: center !important;
    flex-direction: row !important;
}

.vue-form-wizard .wizard-card-footer .wizard-footer-left,
.vue-form-wizard .wizard-card-footer .wizard-footer-right {
    float: none !important;
    flex: 1 !important;
    display: flex !important;
    justify-content: center !important;
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
</style>
