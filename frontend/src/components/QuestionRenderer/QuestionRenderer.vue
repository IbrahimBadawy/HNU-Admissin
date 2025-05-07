<!-- QuestionRenderer.vue -->
<template>
    <div>
        <component :is="componentType" :mode="mode" v-bind="propsToPass" />
    </div>
</template>

<script setup>
    import { computed } from 'vue';
    import TextInput from './types/TextInput.vue';
    import TextArea from './types/TextArea.vue';
    import SelectInput from './types/SelectInput.vue';
    import RadioInput from './types/RadioInput.vue';
    import CheckboxInput from './types/CheckboxInput.vue';
    import DateInput from './types/DateInput.vue';
    import FileUploadInput from './types/FileUploadInput.vue';
    import DraggableInput from './types/DraggableInput.vue';
    import PaymentInput from './types/PaymentInput.vue';
    import OptionsComp from './types/Options.vue';

    const props = defineProps({
        type: { type: String, required: true },
        q_type: { type: String, required: false },
        question: { type: Object, default: () => ({}), required: false },
        mode: { type: String, required: true }, // 'create' | 'edit' | 'view'
        modelValue: [String, Number, Array, Object, File],
        configs: { type: Object, default: () => ({}) },
        meta_data: { type: Object, default: () => ({}) },
        options: { type: Array, default: () => [] },
        option: { type: Object, default: () => ({}) },
        errorState: { type: Boolean, default: false },
    });

    const emits = defineEmits([
        'update:modelValue',
        'update:configs', // ✅ أضف دي
        'update:errorState',
    ]);

    const componentMap = {
        text: TextInput,
        textarea: TextArea,
        select: SelectInput,
        radio: RadioInput,
        checkbox: CheckboxInput,
        date: DateInput,
        'file-upload': FileUploadInput,
        draggable: DraggableInput,
        payment: PaymentInput,
        optionsComp: OptionsComp,
    };

    const componentType = computed(() => componentMap[props.type] || TextInput);

    const propsToPass = computed(() => ({
        modelValue: props.modelValue,
        'onUpdate:modelValue': (val) => emits('update:modelValue', val),
        'onUpdate:errorState': (val) => emits('update:errorState', val),
        'onUpdate:configs': (val) => emits('update:configs', val), // ✅ أضف دي

        configs: props.configs,
        options: props.options,
        mode: props.mode,
        q_type: props.q_type,
        option: props.option,
        question: props.question,
        meta_data: props.meta_data,
    }));
</script>
