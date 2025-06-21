<template>
    <!-- 🟢 create mode -->

    <div v-if="mode === 'create'">
        <label class="block mb-2">اختر سؤال البرنامج</label>

        <select v-model="configsLocal.selectedQuestionTitle" @change="updateQuestion($event.target.value)"
            class="input">
            <option disabled value="">-- اختر سؤالاً --</option>
            <option v-for="(item, index) in questionAnswers" :key="index" :value="item.question_title">
                {{ item.question_title }}
            </option>
        </select>
        <label class="block mb-2">اختر نوع المصروفات</label>

        <select v-model="configsLocal.selectedQuestionType" @change="updateQuestionType($event.target.value)"
            class="input">
            <option disabled value="">-- اختر نوع المصروفات --</option>
            <option v-for="(item, index) in feesTypes" :key="item.id" :value="item.id">
                {{ item.title }}
            </option>
        </select>
        <!-- <label class="block mb-2">المبلغ المطلوب دفعه</label>

        <input type="number" v-model.number="configsLocal.amount" class="input w-full"
            @input="updateAmount($event.target.value)" min="0" placeholder="أدخل المبلغ" /> -->
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <!-- 🟡 edit mode -->
    <div v-else-if="mode === 'edit'">
        <div v-if="!busy">

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
        <div v-else>
            <p>جاري تحميل المصروفات</p>
        </div>
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

const answers = reactive({});
const questions = reactive({});



const selectedFeeType = ref('');
const fetchFeesTypes = async () => {
    const res = await axios.get('/api/payments/fees-types/');
    feesTypes.value = res.data.results || res.data;
};





const route = useRoute();
const error = ref(null);
const loading = ref(false);
const busy = ref(true);

// ✅ local reactive configs
const configsLocal = computed({
    get: () => props.configs || {},
    set: (val) => emit('update:configs', val),
});

watch(
    () => props.configs,
    (newConfigs) => {
        configsLocal.amount = newConfigs.amount || 0;
        configsLocal.selectedQuestionTitle = newConfigs.selectedQuestionTitle || '';
        configsLocal.selectedQuestionType = newConfigs.selectedQuestionType || '';
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

const bankFee = computed(() => Math.round((configsLocal.value.amount * 0.01 + 2) * 100) / 100);
const totalAmount = computed(() => Number(configsLocal.value.amount) + bankFee.value);
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
function updateQuestion(val) {
    emit('update:configs', {
        ...configsLocal.value,
        selectedQuestionTitle: val,

    });
}
function updateQuestionType(val) {
    emit('update:configs', {
        ...configsLocal.value,
        selectedQuestionType: val,

    });
}

function validateAmount() {
    error.value = validateValue(configsLocal.paid, configsLocal.rules || [], 'text');
    emit('update:errorState', !!error.value);
}

async function handlePay() {
    loading.value = true;
    const act_fees = []
    try {

        for (const fee of matchedFees.value) {
            try {
                const params = {
                    submission_id: Number(route.params.id),
                    description: fee.description,
                    amount: fee.amount,
                    fee_list_id: fee.id,  // تأكد أن اسم المفتاح مطابق لما يُطلب في الـ backend
                }
                // console.log(params)
                const act_fee = await axios.post('/api/payments/fees/add-to-submission/',params );
                act_fees.push(act_fee.data)
                // console.log(act_fees)
            } catch (error) {
                // console.error(`فشل إرسال الرسوم (${fee.description}):`, error);
                // يمكنك أيضًا استخدام showToast أو أي إشعار للتنبيه
            }
        }

        const payRes = await axios.post('/api/payments/initiate/', {
            fee_ids:act_fees.map(fee => fee.id),
            form_id: route.params.formId,
            submission_id: route.params.id,
            // tab_id: route.params.tabId,
            order_type: getSelectedFeeTypeTitle(configsLocal.value.selectedQuestionType),
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



const formId = route.params.formId;
const submissionId = route.params.id;
const selectedProgramId = ref(null); // ← ناتج المطابقة
const academicYearId = ref(null); // ← ممكن تحديدها من config أو props

const questionAnswers = ref([]);
const all_questions = ref([]);
const programFees = ref([]);
const matchedFees = ref([]);
const feesTypes = ref([]);
const selectedFeeId = ref(null);

const fetchFormQuestions = async () => {
    const resQA = await axios.get(`/api/admissions/forms/${formId}/unique-questions-answers/`);
    const resForm = await axios.get(`/api/admissions/forms/${formId}/`);

    questionAnswers.value = resQA.data;
    academicYearId.value = resForm.data.academic_year;
}
const calculate_amount = async () => {
    busy.value = true;

    if (configsLocal.value.selectedQuestionTitle && configsLocal.value.selectedQuestionType) {
        const selectedQuestionText = configsLocal.selectedQuestionTitle;
        const storedAnswers = localStorage.getItem('answers');

        const storedQuestions = localStorage.getItem('questions');
        if (storedQuestions) {
            Object.assign(questions, JSON.parse(storedQuestions));
        }
        if (storedAnswers) {
            Object.assign(answers, JSON.parse(storedAnswers));
        }

        const questionId = Object.keys(questions).find(key => questions[key] === selectedQuestionText);
        if (!questionId) return;

        // 2. Get answer to that question
        const selectedAnswer = answers[questionId];
        if (!selectedAnswer) return;

        // 3. Match program by answer text
        const programOptions = await fetchProgramsFromAnswers();
        const matchedProgram = programOptions.find(
            opt => opt.label === selectedAnswer
        );
        if (!matchedProgram) return;

        selectedProgramId.value = matchedProgram.value;


        // 4. Get related program-fees
        const pfRes = await axios.get('/api/payments/program-fees/', {
            params: {
                academic_year: academicYearId.value || '',
                program: selectedProgramId.value,
            },
        });

        const allFees = pfRes.data.results || pfRes.data;

        const flRes = await axios.get('/api/payments/fees-list/')
        const allFeesTypes = flRes.data.results || flRes.data;


        // 5. Filter by fee_type
        matchedFees.value = allFees.filter(fee => {
            const feeListInfo = allFeesTypes.find(f => f.id === fee.fee_list);
            fee.description = feeListInfo?.fees_types?.title
            fee.type_value = feeListInfo?.fees_types?.value
            return feeListInfo?.fees_types?.id === configsLocal.selectedQuestionType;
        });
        console.log(matchedFees.value)
        // 6. Sum amounts
        const totalAmounts = matchedFees.value.reduce((acc, fee) => acc + parseFloat(fee.amount), 0);
        configsLocal.value.amount = totalAmounts;

        updateAmount(totalAmounts)

        busy.value = false;
    }

}

function getSelectedFeeTypeTitle(val) {
  const type = feesTypes.value.find(t => t.id === val);
  return type ? type.value : '';
}
const fetchProgramsFromAnswers = async () => {
    const resFac = await axios.get('/api/users/faculties/');
    const resProg = await axios.get('/api/users/programs/');
    const resQA = await axios.get(`/api/admissions/forms/${formId}/unique-questions-answers/`);

    const faculties = resFac.data.results || resFac.data;
    // console.log(faculties)
    const programs = resProg.data.results || resProg.data;
    questionAnswers.value = resQA.data;

    const options = [];

    faculties.forEach(fac => {
        const facProgs = programs.filter(p => p.faculty === fac.id || p.faculty?.id === fac.id);
        facProgs.forEach(prog => {
            options.push({
                label: `${fac.name} - ${prog.name}`,
                value: prog.id,
                facName: fac.name,
                progName: prog.name,
                sisCode: prog.sis_code || '',
            });
        });
    });

    return options;
};

onMounted(async () => {
    await fetchFormQuestions();
    await fetchFeesTypes();
    await calculate_amount();

    const orderId = route.query.order_id;
    const submission_id = route.params.id;

    // if (submission_id) {
    //     // console.log(submission_id);
    //     // if (props.modelValue !== "true") {
    //     if (true) {

    //         try {
    //             checkingPayment.value = true; // ⬅️ بداية الفحص

    //             const params = {
    //                 submission__id: submission_id,

    //             }

    //             const res = await axios.get(`api/payments/orders/`, { params })


    //             const orders = res.data.results;
    //             // console.log(res.data)
    //             // console.log(res.data.results);


    //             if (orders.length > 0) {
    //                 for (const order of orders) {
    //                     if (order.id) {
    //                         const check = await axios.get(`/api/payments/check/${order.id}/`);
    //                         if (check.data.success) {
    //                             configsLocal.value.paid = true;
    //                             // await axios.patch(`api/admissions/submissions/${submission_id}/`, {
    //                             //     is_paied: true,
    //                             // });
    //                             // props.modelValue = "true";
    //                             new_modelValue.value = true;
    //                             emit('update:modelValue', "true");
    //                             // showToast('تم الدفع بنجاح ✅', 'success');
    //                             break; // ❗ كفاية أول عملية ناجحة
    //                         }
    //                     }
    //                 }
    //             } else {

    //                 // console.log(res.data.results);
    //                 new_modelValue.value = false;
    //                 // props.modelValue = "false";
    //                 emit('update:modelValue', "false");
    //                 // showToast('لا يوجد طلبات دفع مرتبطة ❌', 'error');
    //             }
    //             checkingPayment.value = false; // ⬅️ نهاية الفحص
    //         } catch (err) {
    //             console.error(err);
    //             showToast('حدث خطأ أثناء التحقق من الدفع ❌', 'error');
    //         }
    //     }
    // }

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
