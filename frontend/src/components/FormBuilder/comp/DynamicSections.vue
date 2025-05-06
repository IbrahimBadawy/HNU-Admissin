<template>
    <div class="space-y-4">
        <draggable v-model="localTabs" handle=".handle-tab" group="tabs" @end="updateOrder">
            <template v-for="(tab, i) in localTabs" :key="i">
                <div class="border border-[#d3d3d3] rounded dark:border-[#1b2e4b] m-2">
                    <button
                        class="p-1 w-full flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 text-white-dark dark:bg-[#1b2e4b]"
                        :class="{ '!text-primary': accordians1 === i }"
                    >
                        <label class="flex ml-3 pt-2 w-200"> {{ `القسم الرئيسي # ${i + 1}` }}</label>

                        <input @click="accordians1 = i" v-model="tab.title" class="input w-full" placeholder="عنوان القسم" />
                        <div class="flex gap-2 ml-2">
                            <div @click="accordians1 = i" class="flex gap-2 ml-2">
                                <button @click="addSection(tab)"  class="w-15">+ قسم فرعي</button>
                                <button @click="copyTab(i)" class="w-15">📄 نسخ</button>
                                <button @click="removeTab(i)" class="w-15">🗑 حذف</button>
                            </div>
                            <span @click="accordians1 = -1" class="handle-tab cursor-move pt-4">↕️</span>
                            <div
                                class="w-full sm:w-10 flex justify-start sm:justify-center items-center shrink-0 transition-transform"
                                :class="{ 'rotate-180': accordians1 === i }"
                            >
                                <label @click="accordians1 === i ? (accordians1 = null) : (accordians1 = i)">V</label>
                            </div>
                        </div>
                    </button>
                    <div class="mr-4 card flex mb-3">
                        <label class="ml-3 pt-2"> اختر سؤال الربط</label>
                      
                        <Select @click="accordians1 = i" showClear  v-model="tab.meta_data.depend_question" :options="extractTitlesFromTabs(localTabs)" optionLabel="name" placeholder="اختر سؤال الربط" class="w-full md:w-56" />

                    </div>
                    <vue-collapsible :isOpen="accordians1 === i">
                        <div @click="accordians1 = i" class="space-y-2 p-4 text-white-dark text-[13px] border-t border-[#d3d3d3] dark:border-[#1b2e4b]">
                            <draggable v-model="tab.sections" handle=".handle-section" group="sections" @end="() => updateOrder(tab.sections)">
                                <template v-for="(section, j) in tab.sections" :key="j">
                                    <div class="border border-[#d3d3d3] rounded dark:border-[#1b2e4b] m-2">
                                        <button
                                            type="button"
                                            class="p-1 w-full flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 text-white-dark dark:bg-[#1b2e4b]"
                                            :class="{ '!text-primary': accordians2 === j }"
                                        >
                                            <label class="flex ml-3 pt-2 w-200"> {{ `القسم الفرعي # ${i + 1} - ${j + 1}` }}</label>

                                            <input @click="accordians2 = j" v-model="section.title" class="input w-full" placeholder="عنوان القسم الفرعي" />
                                            <div class="flex gap-2 ml-2" :class="{ '!text-primary': accordians2 === j }">
                                                <button @click="addQuestion(section)" class="w-15">+ سؤال</button>
                                                <button @click="copySection(tab, j)" class="w-15">📄 نسخ</button>
                                                <button @click="removeSection(tab, j)" class="w-15">🗑 حذف</button>
                                                <span @click="accordians2 = -1" class="handle-section cursor-move">↕️</span>
                                                <div
                                                    class="w-full sm:w-10 flex justify-start sm:justify-center items-center shrink-0 transition-transform"
                                                    :class="{ 'rotate-180': accordians2 === j }"
                                                >
                                                    <label @click="accordians2 === j ? (accordians2 = null) : (accordians2 = j)">V</label>
                                                </div>
                                            </div>
                                        </button>
                                        <vue-collapsible :isOpen="accordians2 === j">
                                            <div
                                                @click="accordians2 = j"
                                                class="space-y-2 p-4 text-white-dark text-[13px] border-t border-[#d3d3d3] dark:border-[#1b2e4b]"
                                            >
                                                <draggable
                                                    v-model="section.questions"
                                                    handle=".handle-question"
                                                    group="questions"
                                                    @end="() => updateOrder(section.questions)"
                                                >
                                                    <template v-for="(question, q) in section.questions" :key="q">
                                                        <QuestionEditor
                                                            v-model:title="question.title"
                                                            v-model:id="question.id"
                                                            :k="q"
                                                            :i="i"
                                                            :tab="tab"
                                                            :question="question"
                                                            v-model:meta_data="question.meta_data"
                                                            :tabs="localTabs"
                                                            v-model:required="question.is_required"
                                                            v-model:type="question.question_type"
                                                            v-model:options="question.options"
                                                            v-model:configs="question.configs"
                                                            @remove="() => removeQuestion(section, q)"
                                                            @duplicate="() => copyQuestion(section, q)"
                                                            @update:configs="(val) => question.configs = val"

                                                        />
                                                    </template>
                                                </draggable>
                                            </div>
                                        </vue-collapsible>
                                    </div>
                                </template>
                            </draggable>
                        </div>
                    </vue-collapsible>
                </div>
            </template>
        </draggable>

        <div class="text-center">
            <button class="btn btn-primary mt-4" @click="addTab">+ اضف قسم جديد</button>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, nextTick, onMounted } from 'vue';
    import { VueDraggableNext as draggable } from 'vue-draggable-next';
    import QuestionEditor from './QuestionEditor.vue';
    import VueCollapsible from 'vue-height-collapsible/vue3';
    const accordians1 = ref(0);
    const accordians2 = ref(0);
    const listOfQuestions = ref([]);
    const selectedValue = ref(null);

    const props = defineProps({
        tabs: Array,
    });
    const emit = defineEmits(['update:tabs']);

    const localTabs = ref([]);
    const tree = ref([]);
    const isInternalUpdate = ref(false);
    const featchData = () => {
        selectedValue.value = props.taba.meta_data.depend_question;
    };

    // Sync props.tabs to localTabs, avoiding loops
    watch(
        () => props.tabs,
        (newTabs) => {
            if (JSON.stringify(newTabs) === JSON.stringify(localTabs.value)) return;
            isInternalUpdate.value = true;
            localTabs.value = JSON.parse(JSON.stringify(newTabs));
            nextTick(() => {
                isInternalUpdate.value = false;
            });
        },
        { deep: true, immediate: true }
    );

    // Emit changes when localTabs is modified
    // watch(
    //     () => localTabs.value,
    //     (newValue) => {
    //         if (!isInternalUpdate.value) {
    //             emit('update:tabs', JSON.parse(JSON.stringify(newValue)));
    //         }
    //     },
    //     { deep: true }
    // );

    watch(
        () => localTabs.value,
        (newValue) => {
            if (!isInternalUpdate.value && JSON.stringify(newValue) !== JSON.stringify(props.tabs)) {
                emit('update:tabs', JSON.parse(JSON.stringify(newValue)));
            }
        },
        { deep: true }
    );
    // watch(selectedValue, (val) => {
    //     console.log('Selected Value:', val);
    //     console.log('Selected Question Info:', findQuestionByKey(localTabs.value, val));
    // });

    const updateOrder = (list) => {
        localTabs.value.forEach((item, index) => (item.order = index + 1));
    };

    // Remove all updateTabs() calls from functions below

    function addTab() {
        localTabs.value.push({
            title: '',
            order: localTabs.value.length + 1,
            meta_data: {
                depend_question: '',
            },
            sections: [],
        });
    }

    function changeSelectedValue(val, tab) {
        if (!tab.meta_data) tab.meta_data = {};
        tab.meta_data.depend_question = val;
    }
    function removeTab(index) {
        localTabs.value.splice(index, 1);
    }

    function copyTab(index) {
        const clone = JSON.parse(JSON.stringify(localTabs.value[index]));
        localTabs.value.splice(index + 1, 0, clone);
        updateOrder(localTabs.value);
    }

    function addSection(tab) {
        tab.sections.push({
            title: '',
            order: tab.sections.length + 1,
            questions: [],
        });
    }

    function removeSection(tab, index) {
        tab.sections.splice(index, 1);
        updateOrder(tab.sections);
    }

    function copySection(tab, index) {
        const clone = JSON.parse(JSON.stringify(tab.sections[index]));
        tab.sections.splice(index + 1, 0, clone);
        updateOrder(tab.sections);
    }

    function addQuestion(section) {
        section.questions.push({
            title: '',
            question_type: 'text',
            is_required: false,
            meta_data: {
                depend_question: '',
                description: '',
            },
            order: section.questions.length + 1,
            options: [],
            configs: [],
        });
    }

    function removeQuestion(section, index) {
        section.questions.splice(index, 1);
        updateOrder(section.questions);
    }

    function copyQuestion(section, index) {
        const clone = JSON.parse(JSON.stringify(section.questions[index]));
        section.questions.splice(index + 1, 0, clone);
        updateOrder(section.questions);
    }
    // onMounted(featchData)
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
                    const dat= `${tab.title} | ${section.title} | ${question.title}`
                    result.push({name:dat, code:dat});
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
