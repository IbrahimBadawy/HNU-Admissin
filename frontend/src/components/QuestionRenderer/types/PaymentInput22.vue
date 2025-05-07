<template>
    <!-- 🟢 create mode -->
    <div v-if="mode === 'create'">
        <label class="block mb-2">المبلغ المطلوب دفعه</label>
        <input type="number" v-model.number="amount" class="input w-full" min="0" @input="updateAmount" placeholder="أدخل المبلغ" />
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
        <Validator :rules="configs.rules || []" :questionType="'text'" @update:rules="(val) => updateConfig({ rules: val })" />
    </div>

    <!-- 🟡 edit mode -->
    <div v-else-if="mode === 'edit'">
        <div class="mb-2">
            <span>المبلغ الأساسي: {{ amount }} جنيه</span><br />
            <span>الرسوم البنكية: {{ bankFee }} جنيه</span><br />
            <strong>الإجمالي: {{ totalAmount }} جنيه</strong>
        </div>

        <button v-if="!configs.paid" class="btn btn-primary" @click="handlePay" :disabled="loading">
            {{ loading ? 'جاري التحويل...' : 'الدفع الآن' }}
        </button>

        <p v-else class="text-green-600 mt-2">تم الدفع بنجاح ✅</p>
    </div>

    <!-- 🔵 view mode -->
    <div v-else-if="mode === 'view'">
        <div class="mb-2">
            <span>المبلغ: {{ amount }} جنيه</span><br />
            <span :class="configs.paid ? 'text-green-600' : 'text-red-600'"> حالة الدفع: {{ configs.paid ? 'مدفوع ✅' : 'لم يتم الدفع ❌' }} </span>
        </div>
    </div>

    <!-- ⚙️ تصميم السؤال -->
    <div v-else></div>
</template>
<script setup>
    import { ref, watch, computed, onMounted, reactive, toRefs, watchEffect } from 'vue';
    import { useRoute } from 'vue-router';
    import axios from 'axios';
    import Validator from '../Validator.vue';
    import { validateValue } from '../utils/validation';
    import { showToast } from '@/services/ToastService';

    const props = defineProps(['modelValue', 'mode', 'configs', 'question', 'errorState']);
    const emit = defineEmits(['update:modelValue', 'update:configs', 'update:errorState']);
    const internalConfig = reactive({ ...props.configs });

    watchEffect(() => {
        emit('update:configs', { ...internalConfig });
    });

    const amount = ref(Number(internalConfig.amount || 0));

    watch(
        amount,
        () => {
            error.value = validateValue(amount.value, internalConfig.rules || [], 'text');
            emit('update:errorState', !!error.value);

            updateConfig({
                amount: amount.value,
                pay_amount: totalAmount.value,
                submission_id: route.params.id,
            });
        },
        { immediate: true }
    );

    const route = useRoute();

    const error = ref(null);
    const loading = ref(false);
    const totalAmount = computed(() => Number(amount.value) + bankFee.value);

    function updateConfig(patch) {
        const newConfig = { ...(props.configs || {}), ...patch };
        emit('update:configs', newConfig);
    }

    function updateAmount() {
        error.value = validateValue(amount.value, props.configs?.rules || [], 'text');
        emit('update:errorState', !!error.value);
        updateConfig({
            amount: amount.value,
            pay_amount: totalAmount.value,
            submission_id: route.params.id,
        });
    }

    watch(amount, () => updateAmount(), { immediate: true });

    const bankFee = computed(() => Math.round((amount.value * 0.01 + 2) * 100) / 100);

    async function handlePay() {
        loading.value = true;
        try {
            const feeRes = await axios.post('/api/payments/fees/', {
                submission_id: route.params.id,
                description: 'رسوم تقديم',
                amount: amount.value,
            });
            const feeId = feeRes.data.id;

            const payRes = await axios.post('/api/payments/initiate/', {
                fee_ids: [feeId],
            });

            localStorage.setItem('pending_payment_order', payRes.data.order_id);
            window.location.href = payRes.data.redirect_url;
        } catch (e) {
            console.error(e);
            error.value = 'فشل في بدء الدفع';
        } finally {
            loading.value = false;
        }
    }

    onMounted(async () => {
        const orderId = localStorage.getItem('pending_payment_order');
        if (!orderId) return;

        try {
            const res = await axios.get(`/api/payments/check/${orderId}`);
            const success = res.data.success;
            if (success) {
                emit('update:modelValue', true);
                updateConfig({ paid: true });
                showToast('تم الدفع بنجاح ✅', 'success');
            } else {
                emit('update:modelValue', false);
                updateConfig({ paid: false });
                showToast('فشل التحقق من الدفع ❌', 'error');
            }

            emit('update:modelValue', success); // ✅ true أو false
            updateConfig({ paid: success });
        } catch (e) {
            console.error('فشل التحقق من الدفع', e);
        } finally {
            localStorage.removeItem('pending_payment_order');
        }
    });
</script>

<style scoped>
    .input {
        @apply border border-gray-300 rounded px-2 py-1;
    }
    .btn {
        @apply bg-blue-600 text-white px-4 py-2 rounded mt-2;
    }
</style>
