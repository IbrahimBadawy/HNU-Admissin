<template>
    <div class="p-6 space-y-6">
        <h2 class="text-2xl font-bold">الأعوام الأكاديمية</h2>
        <form @submit.prevent="createYear" class="flex flex-wrap gap-2">
            <input v-model="newYear.name" class="form-input flex-1" placeholder="اسم العام" />
            <input v-model="newYear.start_date" type="date" class="form-input" />
            <input v-model="newYear.end_date" type="date" class="form-input" />
            <button type="submit" class="btn btn-primary">إضافة</button>
        </form>

        <div v-for="year in years" :key="year.id" class="border rounded p-4 space-y-2">
            <div class="flex justify-between items-center">
                <div v-if="!year.editing" class="font-semibold">
                    {{ year.name }} ({{ year.start_date }} - {{ year.end_date }})
                </div>
                <div v-else class="flex flex-wrap gap-2 flex-1">
                    <input v-model="year.editName" class="form-input flex-1" placeholder="اسم العام" />
                    <input v-model="year.editStart" type="date" class="form-input" />
                    <input v-model="year.editEnd" type="date" class="form-input" />
                </div>
                <div class="flex gap-1">
                    <button v-if="!year.editing" class="btn btn-sm" @click="startEdit(year)">تعديل</button>
                    <button v-if="year.editing" class="btn btn-sm btn-primary" @click="updateYear(year)">حفظ</button>
                    <button v-if="year.editing" class="btn btn-sm" @click="cancelEdit(year)">إلغاء</button>
                    <button class="btn btn-sm text-red-500" @click="deleteYear(year.id)">حذف</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/services/axios';

const years = ref([]);
const newYear = ref({ name: '', start_date: '', end_date: '' });

const fetchYears = async () => {
    const res = await axios.get('/api/coordination/academic-years/');
    const data = res.data.results || res.data;
    years.value = data.map(y => ({
        ...y,
        editName: y.name,
        editStart: y.start_date,
        editEnd: y.end_date,
        editing: false,
    }));
};

const createYear = async () => {
    if (!newYear.value.name) return;
    await axios.post('/api/coordination/academic-years/', newYear.value);
    newYear.value = { name: '', start_date: '', end_date: '' };
    fetchYears();
};

const startEdit = (year) => {
    year.editName = year.name;
    year.editStart = year.start_date;
    year.editEnd = year.end_date;
    year.editing = true;
};

const cancelEdit = (year) => {
    year.editing = false;
};

const updateYear = async (year) => {
    await axios.put(`/api/coordination/academic-years/${year.id}/`, {
        name: year.editName,
        start_date: year.editStart,
        end_date: year.editEnd,
    });
    year.editing = false;
    fetchYears();
};

const deleteYear = async (id) => {
    await axios.delete(`/api/coordination/academic-years/${id}/`);
    fetchYears();
};

onMounted(fetchYears);
</script>