<template>
    <div v-if="mode === 'edit'">
        <label v-for="opt in options" :key="opt.title" class="mr-4">
            <div v-if="!opt.meta_data.is_locked">
                <input type="radio" :value="opt.title" :checked="modelValue === opt.title" @change="handleInput" /> {{ opt.title }}
            </div>
            <div v-else>
                {{ `${opt.title} ( ${question.meta_data.depend_question.name.split('|')[2]} لا يسمح)` }}
            </div>
        </label>
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <div v-else-if="mode === 'view'">{{ displayLabel }}</div>

    <div v-else>
        <Validator :rules="configs.rules || []" :questionType="'radio'" @update:rules="(val) => (config.rules = val)" />
    </div>
</template>

<script setup>
    import { ref, watch, computed } from 'vue';
    import Validator from '../Validator.vue';
    import { validateValue } from '../utils/validation';

    const props = defineProps(['modelValue', 'mode', 'configs', 'options', 'errorState', 'question']);
    const emit = defineEmits(['update:modelValue', 'update:errorState']);

    const error = ref(null);

    function handleInput(e) {
        const val = e.target.value;
        emit('update:modelValue', val);

        error.value = validateValue(val, props.config?.rules || [], 'text');
        emit('update:errorState', !!error.value);
    }

    const displayLabel = computed(() => {
        return props.configs.options?.find((o) => o.title === props.modelValue)?.title || props.modelValue;
    });
</script>
