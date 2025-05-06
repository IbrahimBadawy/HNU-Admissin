<template>
    <div class="border border-[#d3d3d3] rounded dark:border-[#1b2e4b] m-2">
        <button
            type="button"
            class="p-1 w-full flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 text-white-dark dark:bg-[#1b2e4b]"
            :class="{ '!text-primary': accordians3 === k }"
        >
            <label @click="accordians3 = k" class="flex items-center"> سؤال</label>
            <input @click="accordians3 = k" v-model="titleValue" class="input w-full" placeholder="عنوان السؤال" />
            <div class="flex gap-2 ml-2" :class="{ '!text-primary': accordians3 === k }">
                <select @click="accordians3 = k" v-model="typeValue" class="input w-32">
                    <option value="text">نص</option>
                    <option value="textarea">فقرة</option>
                    <option value="radio">اختيار واحد</option>
                    <option value="checkbox">اختيارات متعددة</option>
                    <option value="select">قائمة منسدلة</option>
                    <!-- <option value="draggable">ترتيب</option> -->
                    <option value="payment">دفع الكتروني</option>
                    <option value="file-upload">ملف</option>
                    <option value="date">تاريخ</option>
                </select>
                <label @click="accordians3 = k" class="flex items-center">
                    <input @change="changeReq" type="checkbox" v-model="requiredValue" class="mr-1" /> مطلوب
                </label>
                <button @click="$emit('duplicate')" class="w-15">📄</button>
                <button @click="$emit('remove')" class="w-15">🗑</button>
                <span @click="accordians3 = -1" class="w-15handle-question cursor-move">↕️</span>

                <div
                    class="w-full sm:w-10 flex justify-start sm:justify-center items-center shrink-0 transition-transform"
                    :class="{ 'rotate-180': accordians3 === k }"
                >
                    <label @click="accordians3 === k ? (accordians3 = null) : (accordians3 = k)">V</label>
                </div>
            </div>
        </button>
        <div class="mr-4 card flex items-center gap-4 mb-3">
            <!-- 📝 وصف السؤال -->
            <div class="flex-1 flex items-center gap-2">
                <label @click="accordians3 = k" class="whitespace-nowrap">وصف السؤال</label>
                <input @click="accordians3 = k" v-model="descValue" class="input w-full" placeholder="وصف السؤال" />
            </div>

            <!-- 🔗 سؤال الربط -->
            <div class="w-1/3 flex items-center gap-2">
                <label class="whitespace-nowrap">اختر سؤال الربط</label>
                <Select
                    @click="accordians3 = k"
                    showClear
                    v-model="question.meta_data.depend_question"
                    :options="extractTitlesFromTabs(tabs) || { name: '', code: '' }"
                    optionLabel="name"
                    placeholder="اختر سؤال الربط"
                    class="w-full"
                />
            </div>
        </div>

        <vue-collapsible :isOpen="accordians3 === k">
            <div @click="accordians3 = k" class="space-y-2 p-4 text-white-dark text-[13px] border-t border-[#d3d3d3] dark:border-[#1b2e4b]">
                <QuestionRenderer :type="type" :mode="'create'" :question="props.question" :configs="props.configs || {}" />
                <!-- اختيارات إن وجد -->
                <OptionEditor
                    v-if="['radio', 'checkbox', 'select', 'draggable'].includes(typeValue)"
                    :configs="props.configs || {}"
                    v-model:options="optionsValue"
                    :q_type="type"
                />
            </div>
        </vue-collapsible>
    </div>
</template>

<script setup>
    import { ref, computed, defineProps, defineEmits, watchEffect } from 'vue';
    import OptionEditor from './OptionEditor.vue';
    import QuestionRenderer from '@/components/QuestionRenderer/QuestionRenderer.vue';
    import VueCollapsible from 'vue-height-collapsible/vue3';
    import { integer } from '@vuelidate/validators';

    const accordians3 = ref(0);
    const accordians4 = ref(0);
    const listOfQuestions = ref([]);
    const selectedValue = ref(null);

    const props = defineProps({
        title: String,
        k: integer,
        required: Boolean,
        type: String,
        i: integer,
        question: Object,
        meta_data: Object,
        options: Object,
        tab: Object,
        tabs: Array,
        configs: {
            // 1. تغيير تعريف الـ prop إلى Object مع قيمة افتراضية
            type: Object,
            default: () => ({ rules: [] }),
        },
    });

    const emit = defineEmits(['update:title', 'update:required', 'update:type', 'update:options', 'update:configs', 'remove', 'duplicate', 'update:meta_data']);
    watchEffect(() => {
        if (!props.configs.rules) {
            emit('update:configs', { ...props.configs, rules: [] });
        }
    });
    function changeReq(e) {
        const isChecked = e.target.checked;

        if (!props.configs.rules || !Array.isArray(props.configs.rules)) {
            props.configs.rules = [];
        }

        if (isChecked) {
            // أضف فقط لو مش موجود
            const alreadyExists = props.configs.rules.some((rule) => rule.type === 'required');
            if (!alreadyExists) {
                props.configs.rules.push({
                    type: 'required',
                    value: '',
                    message: '',
                });
            }
        } else {
            // 🗑 احذف كل الـ rules اللي نوعها required
            props.configs.rules = props.configs.rules.filter((rule) => rule.type !== 'required');
        }

        console.log(props.configs.rules);
    }
    function changeSelectedValue(val, tab) {
        if (!tab.meta_data) tab.meta_data = {};
        tab.meta_data.depend_question = val;
    }
    const titleValue = computed({
        get: () => props.title,
        set: (val) => emit('update:title', val),
    });
    const descValue = computed({
        get: () => props.meta_data?.description || '',
        set: (val) => {
            const newMeta = { ...(props.meta_data || {}), description: val };
            emit('update:meta_data', newMeta);
        },
    });
    const requiredValue = computed({
        get: () => props.required,
        set: (val) => emit('update:required', val),
    });
    const typeValue = computed({
        get: () => props.type,
        set: (val) => emit('update:type', val),
    });
    const optionsValue = computed({
        get: () => props.options,
        set: (val) => emit('update:options', val),
    });
    const configsValue = computed({
        get: () => props.configs.rules || [],
        set: (val) => {
            // 3. نسخ عميق للكائن وتحديث القواعد
            const newConfigs = JSON.parse(
                JSON.stringify({
                    ...props.configs,
                    rules: val,
                })
            );
            emit('update:configs', newConfigs);
        },
    });

    function findQuestionByKey(tabs, key) {
        const parts = key.split('-').map(Number);
        const [tabIndex, sectionIndex, questionIndex] = parts;

        const tab = tabs[tabIndex];
        if (!tab) return null;

        const section = tab.sections?.[sectionIndex];
        if (!section) return null;

        const question = section.questions?.[questionIndex];
        if (!question) return null;

        return {
            question_id: question.id,
            question_title: question.title,
            section_id: section.id,
            section_title: section.title,
            tab_id: tab.id,
            tab_title: tab.title,
        };
    }
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

    function convertTabsToTree(tabs, i) {
        listOfQuestions.value = tabs.slice(0, i).map((tab, tabIndex) => ({
            key: `${tabIndex}`,
            label: tab.title,
            data: tab.title,
            selectable: false,
            children: (tab.sections || []).map((section, secIndex) => ({
                key: `${tabIndex}-${secIndex}`,
                label: section.title,
                data: section.title,
                selectable: false,
                children: (section.questions || []).map((question, qIndex) => ({
                    key: `${tabIndex}-${secIndex}-${qIndex}`,
                    label: question.title,
                    data: question.title,
                    selectable: true,
                })),
            })),
        }));
    }
</script>

<style scoped>
    .input {
        @apply border border-gray-300 rounded px-2 py-1;
    }
</style>
