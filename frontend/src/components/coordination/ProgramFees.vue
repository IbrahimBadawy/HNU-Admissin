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
        <optgroup v-for="faculty in groupedPrograms" :label="faculty.name" :key="faculty.id">
          <option v-for="prog in faculty.programs" :key="prog.id" :value="prog.id">
            {{ prog.sis_code }} - {{ prog.name }}
          </option>
        </optgroup>
      </select>
    </div>

    <div v-if="fees.length" class="mt-4">
      <table class="w-full table-auto mb-4">
        <thead>
          <tr>
            <th>نوع المصروف</th>
            <th>المصروف</th>
            <th>القيمة</th>
            <th>إلزامي؟</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fee in fees" :key="fee.id">
            <template v-if="!fee.editing">
              <td>

                  {{ getFeeTypeTitle(fee.fee_list) }}
              </td>
              <td>{{ getFeeTitle(fee.fee_list) }}</td>
              <td>{{ fee.amount }}</td>
              <td><input type="checkbox" disabled :checked="fee.is_requierd" /></td>
              <td class="flex gap-1">
                <button class="text-blue-500" @click="startFeeEdit(fee)">تعديل</button>
                <button class="text-red-500 mr-4" @click="deleteFee(fee.id)">حذف</button>
              </td>
            </template>
            <template v-else>
              <td>

                <!-- نوع المصروف -->
                <select v-model="fee.edit_fee_type" class="form-select w-full mb-2" @change="onEditFeeTypeChange(fee)">
                  <option disabled value="">اختر نوع المصروف</option>
                  <option v-for="type in feesTypes" :key="type.id" :value="type.id">
                    {{ type.title }}
                  </option>
                </select>
              </td>
              <td>

                <!-- المصروف -->
                <select v-model="fee.edit_fee_list" class="form-select w-full">
                  <option disabled value="">اختر المصروف</option>
                  <option v-for="f in fee.filteredOptions" :key="f.id" :value="f.id">
                    {{ f.title }}
                  </option>
                </select>
              </td>
              <td><input v-model.number="fee.editAmount" type="number" class="form-input w-full" /></td>
              <td><input type="checkbox" v-model="fee.editIsRequired" /></td>
              <td class="flex gap-1">
                <button class="text-green-500" @click="saveFeeEdit(fee)">حفظ</button>
                <button class="text-gray-500 mr-4" @click="cancelFeeEdit(fee)">إلغاء</button>
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>

    <form @submit.prevent="createFee" class="flex flex-wrap gap-2 items-center">
      <select v-model="selectedFeeType" class="form-select flex-1">
        <option disabled value="">اختر نوع المصروف</option>
        <option v-for="type in feesTypes" :key="type.id" :value="type.id">{{ type.title }}</option>
      </select>
      <select v-model="newFeeList" class="form-select flex-1">
        <option disabled value="">اختر المصروف</option>
        <option v-for="f in feesListOptions" :key="f.id" :value="f.id">{{ f.title }}</option>
      </select>
      <input v-model.number="newFeeAmount" type="number" class="form-input w-32" placeholder="القيمة" />
      <label class="flex items-center gap-1 text-sm">
        <input type="checkbox" v-model="newFeeIsRequired" />
        إلزامي
      </label>
      <button type="submit" class="btn btn-secondary">إضافة</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from '@/services/axios';

const years = ref([]);
const groupedPrograms = ref([]);
const fees = ref([]);
const allFees = ref([]);

const selectedYear = ref('');
const selectedProgram = ref('');
const newFeeList = ref('');
const newFeeAmount = ref(null);
const newFeeIsRequired = ref(false);
const feesListOptions = ref([]);
const feesTypes = ref([]);
const selectedFeeType = ref('');
const fetchFeesTypes = async () => {
  const res = await axios.get('/api/payments/fees-types/');
  feesTypes.value = res.data.results || res.data;
};

const fetchFeesList = async () => {
  const res = await axios.get('/api/payments/fees-list/');
  allFees.value = res.data.results || res.data;
  // console.log(allFees)
  if (selectedFeeType.value) {
    feesListOptions.value = allFees.value.filter(f => f.fees_types?.id === selectedFeeType.value);
  } else {
    feesListOptions.value = allFees.value;
  }
};
const getFilteredFeesByType = (typeId) => {
  if (!typeId) return [];
  return feesListOptions.value.filter(f => f.fees_types?.id === Number(typeId));
};

const fetchYears = async () => {
  const res = await axios.get('/api/users/academic-years/');
  years.value = res.data.results || res.data;
};
function getFeeTitle(feeId) {
  const fee = allFees.value.find(f => f.id === feeId);
  return fee ? fee.title : '';
}
function getFeeTypeTitle(feeListId) {
  const fee = allFees.value.find(f => f.id === feeListId);
  return fee?.fees_types?.title || '';
}
function onEditFeeTypeChange(fee) {
  const typeId = fee.edit_fee_type;
  fee.edit_fee_list = ''; // تصفير المصروف السابق
  fee.filteredOptions = allFees.value.filter(f => f.fees_types?.id === typeId);
}


const fetchPrograms = async () => {
  const resFac = await axios.get('/api/users/faculties/');
  const resProg = await axios.get('/api/users/programs/');
  const faculties = resFac.data.results || resFac.data;
  const programs = resProg.data.results || resProg.data;

  groupedPrograms.value = faculties
    .map(fac => {
      const facPrograms = programs
        .filter(p => p.faculty === fac.id || p.faculty?.id === fac.id)
        .sort((a, b) => (a.sis_code || '').localeCompare(b.sis_code || ''));

      const firstSisCode = facPrograms.length > 0 ? (facPrograms[0].sis_code || '') : '';

      return {
        id: fac.id,
        name: fac.name,
        programs: facPrograms,
        firstSisCode,
      };
    })
    .filter(f => f.programs.length > 0)
    .sort((a, b) => a.firstSisCode.localeCompare(b.firstSisCode));
};

const fetchFees = async () => {
  if (!selectedYear.value || !selectedProgram.value) return;
  const res = await axios.get('/api/payments/program-fees/', {
    params: { academic_year: selectedYear.value, program: selectedProgram.value },
  });
  fees.value = (res.data.results || res.data).map(fee => ({
    ...fee,
    editing: false,
    edit_fee_type: fee.fee_list_data?.fees_types?.id || '',
    edit_fee_list: fee.fee_list,
    editAmount: fee.amount,
    editIsRequired: fee.is_requierd,
    filteredOptions: allFees.value.filter(
      f => f.fees_types?.id === fee.fee_list_data?.fees_types?.id
    ),
  }));

};

const createFee = async () => {
  if (!selectedYear.value || !selectedProgram.value || !newFeeList.value) return;
  await axios.post('/api/payments/program-fees/', {
    academic_year: selectedYear.value,
    program: selectedProgram.value,
    fee_list: newFeeList.value,
    amount: newFeeAmount.value,
    is_requierd: newFeeIsRequired.value,
  });
  newFeeList.value = '';
  newFeeAmount.value = null;
  newFeeIsRequired.value = false;
  fetchFees();
};

const deleteFee = async (id) => {
  await axios.delete(`/api/payments/program-fees/${id}/`);
  fetchFees();
};

const startFeeEdit = (fee) => {
  fee.editing = true;
};

const cancelFeeEdit = (fee) => {
  fee.editing = false;
  fee.edit_fee_list = fee.fee_list;
  fee.editAmount = fee.amount;
  fee.editIsRequired = fee.is_requierd;
};

const saveFeeEdit = async (fee) => {
  await axios.patch(`/api/payments/program-fees/${fee.id}/`, {
    fee_list: fee.edit_fee_list,
    amount: fee.editAmount,
    is_requierd: fee.editIsRequired,
  });
  fetchFees();
};

watch([selectedYear, selectedProgram], ([year, program]) => {
  if (year && program) {
    fetchFees();
  }
});

onMounted(() => {
  fetchYears();
  fetchPrograms();
  fetchFeesTypes();
  fetchFeesList(); // 🆕
});
watch(selectedFeeType, () => {
  fetchFeesList();
});

</script>