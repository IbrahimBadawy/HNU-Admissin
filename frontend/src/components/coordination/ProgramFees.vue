<template>
    <div class="p-6 space-y-6">
        <h2 class="text-2xl font-bold mb-4">مصروفات البرامج</h2>
        <div class="flex flex-wrap gap-4">
            <select v-model="selectedYear" class="form-select">
                <option disabled value="">السنة الدراسية</option>
                <option v-for="y in years" :key="y.id" :value="y.id">{{ y.name }}</option>
            </select>
            <select v-model="selectedProgram" class="form-select">
                <option disabled value="">البرنامج</option>
                <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
            <button class="btn btn-primary" @click="fetchFees">عرض</button>
        </div>

        <div v-if="fees.length" class="mt-4">
            <table class="w-full table-auto mb-4">
                <thead>
                    <tr>
                        <th>الوصف</th>
                        <th>القيمة</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="fee in fees" :key="fee.id">
                        <td>{{ fee.description }}</td>
                        <td>{{ fee.amount }}</td>
                        <td>
                            <button class="text-red-500" @click="deleteFee(fee.id)">حذف</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <form @submit.prevent="createFee" class="flex flex-wrap gap-2">
            <input v-model="newFeeDesc" class="form-input flex-1" placeholder="وصف المصروف" />
            <input v-model.number="newFeeAmount" type="number" class="form-input w-32" placeholder="القيمة" />
            <button type="submit" class="btn btn-secondary">إضافة</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/services/axios';

const years = ref([]);
const programs = ref([]);
const fees = ref([]);

const selectedYear = ref('');
const selectedProgram = ref('');
const newFeeDesc = ref('');
const newFeeAmount = ref(null);

const fetchYears = async () => {
    const res = await axios.get('/api/coordination/academic-years/');
    years.value = res.data.results || res.data;
};

const fetchPrograms = async () => {
    const res = await axios.get('/api/users/programs/');
    programs.value = res.data.results || res.data;
};

const fetchFees = async () => {
    if (!selectedYear.value || !selectedProgram.value) return;
    const res = await axios.get('/api/coordination/program-fees/', {
        params: { academic_year: selectedYear.value, program: selectedProgram.value },
    });
    fees.value = res.data.results || res.data;
};

const createFee = async () => {
    if (!selectedYear.value || !selectedProgram.value || !newFeeDesc.value) return;
    await axios.post('/api/coordination/program-fees/', {
        academic_year: selectedYear.value,
        program: selectedProgram.value,
        description: newFeeDesc.value,
        amount: newFeeAmount.value,
    });
    newFeeDesc.value = '';
    newFeeAmount.value = null;
    fetchFees();
};

const deleteFee = async (id) => {
    await axios.delete(`/api/coordination/program-fees/${id}/`);
    fetchFees();
};

onMounted(() => {
    fetchYears();
    fetchPrograms();
});
</script>