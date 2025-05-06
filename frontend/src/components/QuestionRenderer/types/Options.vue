<template>
    <div class="space-y-2">
        <!-- ⚙️ وضع create -->
        <div v-if="mode == 'create'">
            <Validator
                :rules="option.meta_data.rules || []"
                :questionType="q_type"
                @update:rules="(rules) => (option.meta_data.rules = rules)"
                @update:option="(val) => emit('update:option', val)"
            />
        </div>
    </div>
</template>

<script setup>
    import { ref, defineExpose, watch } from 'vue';
    import Validator from '../Validator.vue';
    import { validateValue } from '../utils/validation';

    const props = defineProps(['modelValue', 'mode', 'configs', 'errorState', 'q_type', 'option']);
    const emit = defineEmits(['update:option']);
</script>

<style scoped>
    .input {
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 6px 10px;
        width: 100%;
    }
</style>
