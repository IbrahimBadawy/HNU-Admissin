<template>
    <div class="space-y-3">
        <div v-for="(rule, index) in rulesLocal" :key="index" class="flex items-center gap-2">
            <select v-model="rule.type" class="input w-40">
                <option v-for="opt in availableRules" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                </option>
            </select>
            <div v-if="needsValue(rule.type)">
                <input v-if="questionType === 'date'" v-model="rule.value" type="date" class="input" placeholder="Value" />
                <input v-else v-model="rule.value" class="input" placeholder="Value" />
            </div>
            <input v-model="rule.message" class="input flex-1" placeholder="رسالة الخطأ (اختياري)" />
            <button @click="removeRule(index)" class="text-red-600">✕</button>
        </div>

        <button @click="addRule" class="btn">+ اضافة شرط</button>
    </div>
</template>

<script setup>
    import { ref, watch, computed } from 'vue';

    const props = defineProps({
        rules: { type: Array, default: () => [] },
        questionType: String,
        option: { type: Object, default: () => ({}) },
    });

    const emit = defineEmits(['update:rules', 'update:option']);

    const rulesLocal = ref(JSON.parse(JSON.stringify(props.rules || [])));

    const safeClone = (obj) => JSON.parse(JSON.stringify(obj));

    // ✅ Sync props.rules → rulesLocal
    watch(
        () => props.rules,
        (newRules) => {
            if (JSON.stringify(newRules) !== JSON.stringify(rulesLocal.value)) {
                rulesLocal.value = safeClone(newRules);
            }
        }
    );

    // ✅ Sync rulesLocal → emits
    watch(
        rulesLocal,
        (newVal) => {
            const cloned = safeClone(newVal);
            emit('update:rules', cloned);

            if (props.option && typeof props.option === 'object') {
                emit('update:option', {
                    ...props.option,
                    meta_data: {
                        ...(props.option.meta_data || {}),
                        rules: cloned,
                    },
                });
            }
        },
        { deep: true }
    );

    function addRule() {
        rulesLocal.value.push({ type: 'required', value: '', message: '' });
    }

    function removeRule(index) {
        rulesLocal.value.splice(index, 1);
    }

    function needsValue(type) {
        return !['required'].includes(type);
    }

    const ruleOptionsMap = {
        text: [
            { value: 'required', label: 'حقل مطلوب' },
            { value: 'minLength', label: 'لا يقل عن' },
            { value: 'maxLength', label: 'لا يزيد عن' },
            { value: 'equal', label: 'يساوي' },
            { value: 'regex', label: 'Regex' },
        ],
        OptionsComp: [
            { value: 'required', label: 'حقل مطلوب' },
            { value: 'minLength', label: 'لا يقل عن' },
            { value: 'maxLength', label: 'لا يزيد عن' },
            { value: 'regex', label: 'Regex' },
        ],
        textarea: [{ value: 'required', label: 'حقل مطلوب' }],
        number: [
            { value: 'required', label: 'حقل مطلوب' },
            { value: 'minLength', label: 'لا يقل عن' },
            { value: 'maxLength', label: 'لا يزيد عن' },
            { value: 'min', label: 'اصغر من' },
            { value: 'max', label: 'اكبر من' },
            { value: 'min_eq', label: 'اصغر من او يساوي' },
            { value: 'max_eq', label: 'اكبر من او يساوي' },
            { value: 'not_eq', label: 'يساوي' },
            { value: 'regex', label: 'Regex' },
        ],
        'file-upload': [
            { value: 'required', label: 'حقل مطلوب' },
            { value: 'maxSize', label: 'اقصى حجم (MB)' },
            { value: 'types', label: 'الأنواع' },
        ],
        checkbox: [
            { value: 'required', label: 'اختر واحد على الاقل' },
            { value: 'min', label: 'لا يقل عن' },
            { value: 'max', label: 'لا يزيد عن' },
            { value: 'equal', label: 'يساوي' },
        ],
        radio: [{ value: 'required', label: 'مطلوب' }],
        select: [{ value: 'required', label: 'مطلوب' }],
        payment: [{ value: 'required', label: 'مطلوب' }],
        draggable: [
            { value: 'required', label: 'اختر واحد على الاقل' },
            { value: 'min', label: 'لا يقل عن' },
            { value: 'max', label: 'لا يزيد عن' },
            { value: 'equal', label: 'يساوي' },
        ],
        date: [
            { value: 'required', label: 'حقل مطلوب' },
            { value: 'minDate', label: 'ابتداءا من تاريخ' },
            { value: 'maxDate', label: 'حتى تاريخ' },
        ],
    };

    const availableRules = computed(() => {
        return ruleOptionsMap[props.questionType] || [{ value: 'required', label: 'مطلوب' }];
    });
</script>

<style scoped>
    .input {
        border: 1px solid #ccc;
        padding: 6px 8px;
        border-radius: 6px;
        min-width: 80px;
    }
    .btn {
        background: #2c7be5;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
    }
</style>
