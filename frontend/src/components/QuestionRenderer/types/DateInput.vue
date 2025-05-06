<template>
    <div v-if="mode === 'edit'">
        <input type="date" class="input" :value="modelValue" @input="handleInput" />
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>

    </div>
    <div v-else-if="mode === 'view'">{{ modelValue }}</div>
    <div v-else-if="mode === 'create'" class="mt-2 text-gray-500">
        <Validator :rules="configs.rules || []" :questionType="'date'" @update:rules="(val) => (configs.rules = val)" />
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import Validator from '../Validator.vue';
    import { validateValue } from '../utils/validation';

    const props = defineProps(['modelValue', 'mode', 'configs', 'errorState']);
    const emit = defineEmits(['update:modelValue', 'update:errorState']);

    const error = ref(null);

    function handleInput(e) {
        const val = e.target.value;
        emit('update:modelValue', val);

        error.value = validateValue(val, props.configs?.rules || [], 'date');
        emit('update:errorState', !!error.value);
    }
</script>
