<template>
    <div v-if="mode === 'edit'">
        <select class="input" :value="modelValue" @change="handleInput">
            <div v-for="opt in options">
                <option v-if="!opt.meta_data.is_locked" :key="opt.title" :value="opt.title">
                    {{ opt.title }}
                </option>
            </div>
        </select>

        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <div v-else-if="mode === 'view'">
        {{ displayLabel }}
    </div>

    <div v-else>
        <Validator :rules="configs.rules || []" :questionType="'select'" @update:rules="(val) => (configs.rules = val)" />
    </div>
</template>

<script setup>
    import { watch, computed, ref, defineExpose } from 'vue';
    import Validator from '../Validator.vue';
    import { validateValue } from '../utils/validation';

    const props = defineProps(['modelValue', 'mode', 'configs', 'options', 'errorState']);
    const emit = defineEmits(['update:modelValue', 'update:errorState']);

    const error = ref(null);

    function handleInput(e) {
        const val = e.target.value;
        // console.log(val);

        emit('update:modelValue', val);

        error.value = validateValue(val, props.configs?.rules || [], 'select');
        emit('update:errorState', !!error.value);
    }

    const displayLabel = computed(() => {
        const match = props.options?.find((o) => o.title === props.modelValue);
        return match?.title || props.modelValue;
    });
</script>
