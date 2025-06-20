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
              <th>الوصف</th>
              <th>القيمة</th>
              <th>إلزامي؟</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fee in fees" :key="fee.id">
              <template v-if="!fee.editing">
                <td>{{ fee.description }}</td>
                <td>{{ fee.amount }}</td>
                <td><input type="checkbox" disabled :checked="fee.is_requierd" /></td>
                <td class="flex gap-1">
                  <button class="text-blue-500" @click="startFeeEdit(fee)">تعديل</button>
                  <button class="text-red-500 mr-4" @click="deleteFee(fee.id)">حذف</button>
                </td>
              </template>
              <template v-else>
                <td><input v-model="fee.editDescription" class="form-input w-full" /></td>
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
        <input v-model="newFeeDesc" class="form-input flex-1" placeholder="وصف المصروف" />
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
  
  const selectedYear = ref('');
  const selectedProgram = ref('');
  const newFeeDesc = ref('');
  const newFeeAmount = ref(null);
  const newFeeIsRequired = ref(false);
  
  const fetchYears = async () => {
    const res = await axios.get('/api/coordination/academic-years/');
    years.value = res.data.results || res.data;
  };
  
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
    const res = await axios.get('/api/coordination/program-fees/', {
      params: { academic_year: selectedYear.value, program: selectedProgram.value },
    });
    fees.value = (res.data.results || res.data).map(fee => ({
      ...fee,
      editing: false,
      editDescription: fee.description,
      editAmount: fee.amount,
      editIsRequired: fee.is_requierd,
    }));
  };
  
  const createFee = async () => {
    if (!selectedYear.value || !selectedProgram.value || !newFeeDesc.value) return;
    await axios.post('/api/coordination/program-fees/', {
      academic_year: selectedYear.value,
      program: selectedProgram.value,
      description: newFeeDesc.value,
      amount: newFeeAmount.value,
      is_requierd: newFeeIsRequired.value,
    });
    newFeeDesc.value = '';
    newFeeAmount.value = null;
    newFeeIsRequired.value = false;
    fetchFees();
  };
  
  const deleteFee = async (id) => {
    await axios.delete(`/api/coordination/program-fees/${id}/`);
    fetchFees();
  };
  
  const startFeeEdit = (fee) => {
    fee.editing = true;
  };
  
  const cancelFeeEdit = (fee) => {
    fee.editing = false;
    fee.editDescription = fee.description;
    fee.editAmount = fee.amount;
    fee.editIsRequired = fee.is_requierd;
  };
  
  const saveFeeEdit = async (fee) => {
    await axios.patch(`/api/coordination/program-fees/${fee.id}/`, {
      description: fee.editDescription,
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
  });
  </script>
  