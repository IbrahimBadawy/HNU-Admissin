<template>
    <!-- 🟢 create mode -->

    <div v-if="mode === 'create'">
        <label class="block mb-2">المبلغ المطلوب دفعه</label>
        <input type="number" v-model.number="configsLocal.amount" class="input w-full"
            @input="updateAmount($event.target.value)" min="0" placeholder="أدخل المبلغ" />
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <!-- 🟡 edit mode -->
    <div v-else-if="mode === 'edit'">
        <div class="mb-2">
            <span>المبلغ الأساسي: {{ configsLocal.amount }} جنيه</span><br />
            <span>الرسوم البنكية: {{ bankFee }} جنيه</span><br />
            <strong>الإجمالي: {{ totalAmount }} جنيه</strong>
        </div>

        <!-- <button v-if="!configsLocal.paid" class="btn btn-primary" @click="handlePay" :disabled="loading"> -->
        <button v-if="!new_modelValue" class="btn btn-primary" @click="handlePay" :disabled="loading">
            {{ loading ? 'جاري التحويل...' : 'الدفع الآن' }}
        </button>

        <p v-else class="text-green-600 mt-2">تم الدفع بنجاح ✅</p>
    </div>

    <!-- 🔵 view mode -->
    <div v-else-if="mode === 'view'">
  <div class="mb-2">
    <span>المبلغ: {{ configsLocal.amount }} جنيه</span><br />

    <span v-if="checkingPayment" class="text-blue-600">💳 جاري الفحص...</span>

    <span v-else :class="new_modelValue ? 'text-green-600' : 'text-red-600'">
      حالة الدفع: {{ new_modelValue ? 'مدفوع ✅' : 'لم يتم الدفع ❌' }}
    </span>
  </div>
</div>

</template>
<script setup>
import { ref, watch, computed, onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import axios from '@/services/axios';
import { validateValue } from '../utils/validation';
import { showToast } from '@/services/ToastService';

const props = defineProps(['modelValue', 'mode', 'configs', 'question', 'errorState']);
const emit = defineEmits(['update:modelValue', 'update:configs', 'update:errorState']);
// const new_modelValue = computed(() => props.modelValue === 'true');
const new_modelValue = ref(false);
const checkingPayment = ref(false);


const route = useRoute();
const error = ref(null);
const loading = ref(false);

// ✅ local reactive configs
const configsLocal = computed({
    get: () => props.configs || {},
    set: (val) => emit('update:configs', val),
});

watch(
    () => props.configs,
    (newConfigs) => {
        configsLocal.amount = newConfigs.amount || 0;
        configsLocal.pay_amount = newConfigs.pay_amount || 0;
        configsLocal.paid = newConfigs.paid || false;
    },
    { immediate: true },
    { deep: true }
);
// ✅ sync back to parent
watch(
    configsLocal,
    (newVal) => {
        emit('update:configs', { ...newVal });
    },
    { deep: true }
);
// watch(
//     props.modelValue,
//     (newVal) => {
//         if(newVal){

//             emit('update:modelValue', { ...newVal });
//         }
//     },
//     { deep: true }
// );

const bankFee = computed(() => Math.round((configsLocal.amount * 0.01 + 2) * 100) / 100);
const totalAmount = computed(() => Number(configsLocal.amount) + bankFee.value);
// ✅ update derived values
watch(
    () => configsLocal.amount,
    () => {
        configsLocal.pay_amount = totalAmount.value;
    },
    { immediate: true }
);

function updateAmount(val) {
    emit('update:configs', {
        ...configsLocal.value,
        amount: val,
        pay_amount: val,
    });
}

function validateAmount() {
    error.value = validateValue(configsLocal.paid, configsLocal.rules || [], 'text');
    emit('update:errorState', !!error.value);
}

async function handlePay() {
    loading.value = true;
    try {
        const feeRes = await axios.post('/api/payments/fees/add-to-submission/', {
            submission_id: Number(route.params.id),
            description: 'رسوم تقديم',
            amount: configsLocal.amount,
        });

        const payRes = await axios.post('/api/payments/initiate/', {
            fee_ids: [feeRes.data.id],
            form_id: route.params.formId,
            submission_id: route.params.id,
            tab_id: route.params.tabId,
        });

        localStorage.setItem('pending_payment_order', payRes.data.order_id);
        window.location.href = payRes.data.redirect_url;
    } catch (e) {
        error.value = 'فشل في بدء الدفع';
        console.error(e);
    } finally {
        loading.value = false;
    }
}

onMounted(async () => {
    const orderId = route.query.order_id;
    const submission_id = route.params.id;

    if (submission_id) {
        // console.log(submission_id);
        // if (props.modelValue !== "true") {
        if (true) {

            try {
                checkingPayment.value = true; // ⬅️ بداية الفحص

                const params = {
                    submission__id: submission_id,

                }

                const res = await axios.get(`api/payments/orders/`, { params })


                const orders = res.data.results;
                // console.log(res.data)
                // console.log(res.data.results);


                if (orders.length > 0) {
                    for (const order of orders) {
                        if (order.id) {
                            const check = await axios.get(`/api/payments/check/${order.id}/`);
                            if (check.data.success) {
                                configsLocal.value.paid = true;
                                // await axios.patch(`api/admissions/submissions/${submission_id}/`, {
                                //     is_paied: true,
                                // });
                                // props.modelValue = "true";
                                new_modelValue.value = true;
                                emit('update:modelValue', "true");
                                // showToast('تم الدفع بنجاح ✅', 'success');
                                break; // ❗ كفاية أول عملية ناجحة
                            }
                        }
                    }
                } else {

                    // console.log(res.data.results);
                    new_modelValue.value = false;
                    // props.modelValue = "false";
                    emit('update:modelValue', "false");
                    // showToast('لا يوجد طلبات دفع مرتبطة ❌', 'error');
                }
                checkingPayment.value = false; // ⬅️ نهاية الفحص
            } catch (err) {
                console.error(err);
                showToast('حدث خطأ أثناء التحقق من الدفع ❌', 'error');
            }
        }
    }

    // if (!new_modelValue.value){
    //     const res = await axios.get(`/api/payments/check/${orderId}/`);


    // }
    if (orderId) {
        try {
            const res = await axios.get(`/api/payments/check/${orderId}/`);
            console.log(orderId)
            console.log(res)
            if (res.data.success) {
                configsLocal.value.paid = true;
                // props.modelValue = "true";
                new_modelValue.value = true;
                emit('update:modelValue', "true");
                showToast('تم الدفع بنجاح ✅', 'success');
            } else {
                // props.modelValue = "false";
                new_modelValue.value = false;
                emit('update:modelValue', "false");
                showToast('فشل الدفع ❌', 'error');
            }
        } catch (e) {
            console.error(e);
            showToast('حدث خطأ أثناء التحقق من الدفع', 'error');
        }
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
