<template>
    <div class="p-4 space-y-6">
        <!-- عرض التابات والسيكشنز والأسئلة -->
        <!-- <div v-if="form">
            <div v-for="tab in form.tabs" :key="tab.id">
                <div v-for="section in tab.sections" :key="section.id">
                    <div v-if="!section.meta_data.is_visible">
                        <div v-for="question in section.questions" :key="question.id">
                            {{ `tab : ${tab.title} | section : ${section.title} | question : ${question.title}` }}
                        </div>
                    </div>
                </div>
            </div>
        </div> -->

        <form-wizard
            v-if="form"
            shape="circle"
            color="#4361ee"
            class="circle"
            @on-complete="submit(false, form.tabs.length + 1, 'end')"
            :start-index="route.params.tabId - 1 || 0"
            step-size="xs"
            nextButtonText="التالي"
            backButtonText="السابق"
            finishButtonText="انهاء"
        >
            <tab-content v-for="tab in form.tabs" :key="tab.id" :title="tab.title" :before-change="() => nextTab(tab)">
                <div v-for="section in tab.sections" :key="section.id" class="mb-4">
                    <div v-if="section.meta_data.is_visible">
                        <h3 class="text-lg font-semibold mb-2">{{ section.title }}</h3>
                        <div v-for="question in section.questions" :key="question.id" class="border p-4 rounded shadow mb-2">
                            <h4 class="font-semibold mb-2">{{ question.title }}</h4>
                            <h4 class="mb-2">{{ question.meta_data.description || '' }}</h4>
                            <QuestionRenderer
                                :type="question.question_type"
                                :mode="mode"
                                :question="question"
                                v-model="answers[question.id]"
                                :configs="question.configs || {}"
                                :options="question.options || []"
                                v-model:errorState="errors[question.id]"
                            />
                        </div>
                    </div>
                </div>
            </tab-content>
        </form-wizard>

        <!-- زر الإرسال في وضع edit -->
        <div v-if="submission_dat" class="mt-6 flex w-full justify-center flex-row">
            <button
                class="btn mr-4"
                v-if="is_staff"
                @click="toggleActive(submission_dat)"
                :title="submission_dat.is_locked ? 'فتح النموذج للطالب' : 'غلق النموذج للطالب'"
            >
                <span v-if="submission_dat.is_locked">فتح</span>
                <span v-else>غلق</span>
            </button>
            <div v-if="mode === 'view'" class="mr-5">
                <button class="btn" @click="goToEdit(formId, submissionId, route.params.tabId || 1)">تعديل ✏️</button>
            </div>
            <div v-if="mode === 'edit' && !route.path.includes('new')" class="mr-5">
                <button class="btn" @click="goToSave(formId, submissionId, route.params.tabId || 1)">حفظ</button>
            </div>
            <div class="mr-5">
                <button class="btn" @click="goToBack(formId)">عودة</button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, reactive, computed, onMounted, watch } from 'vue';
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
    const errors = reactive({});

    const submissionId = ref('');
    const formId = ref('');

    const hasErrors = computed(() => Object.values(errors).includes(true));

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
        const error = checkQuestionsn(tab);
        // console.log(tab.order);
        const atab = checkOptions(tab.order);
        if (!error) {
            const check = tab.order < count_tabs;
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
                        answers[q.id] = '';
                        errors[q.id] = false;
                    });
                });
            });

            // لو تعديل أو عرض، هات البيانات
            if (submissionId.value) {
                const res2 = await axios.get(`api/admissions/submissions/${submissionId.value}/`);
                submission_dat.value = res2.data;
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
                        if (source === 'end' && form.value.tabs.length == 1) {
                            const res = await axios.post('api/admissions/submissions/', payload);
                            formId.value = res.data.form;
                            submissionId.value = res.data.id;
                            router.push(`/submissions/${formId.value}/`);
                        }

                        if (form.value.tabs.length > 1) {
                            const res = await axios.post('api/admissions/submissions/', payload);
                            formId.value = res.data.form;
                            submissionId.value = res.data.id;
                            router.push(`/submissions/${formId.value}/${submissionId.value}/edit/${index}`);
                        }
                    } else {
                        if (route.path.includes('edit')) {
                            if (source === 'end') {
                                await axios.put(`api/admissions/submissions/${submissionId.value}/`, payload);
                                router.push(`/submissions/${formId.value}/`);
                            } else {
                                await axios.put(`api/admissions/submissions/${submissionId.value}/`, payload);
                                router.push(`/submissions/${formId.value}/${submissionId.value}/edit/${index}`);
                            }
                        } else {
                            router.push(`/submissions/${formId.value}/`);
                        }
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
        const res = await axios.post('api/admissions/submissions/', payload);
        formId.value = res.data.form;
        submissionId.value = res.data.id;

        router.push(`/submissions/${f_id}/${s_id}/${t_id}`);
        mode.value = 'view';
    };
    onMounted(async () => {
        await fetchForm();
        updateSectionVisibility();
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
</style>
