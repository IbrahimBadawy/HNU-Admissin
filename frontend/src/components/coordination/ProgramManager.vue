<template>
    <div class="p-6 space-y-6">
        <h2 class="text-2xl font-bold">الكليات والبرامج</h2>
        <form @submit.prevent="createFaculty" class="flex gap-2">
            <input v-model="newFacultyName" class="form-input flex-1" placeholder="اسم الكلية" />
            <button type="submit" class="btn btn-primary">إضافة كلية</button>
        </form>

        <div v-for="faculty in faculties" :key="faculty.id" class="border rounded p-4">
            <div class="font-semibold mb-2">{{ faculty.name }}</div>
            <ul class="space-y-1 mb-2">
                <li v-for="prog in faculty.programs" :key="prog.id" class="flex justify-between">
                    {{ prog.name }}
                </li>
            </ul>
            <form @submit.prevent="createProgram(faculty)" class="flex gap-2">
                <input v-model="faculty.newProgram" class="form-input flex-1" placeholder="اسم البرنامج" />
                <button type="submit" class="btn btn-secondary">إضافة برنامج</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/services/axios';

const faculties = ref([]);
const newFacultyName = ref('');

const fetchFaculties = async () => {
    const resFac = await axios.get('/api/users/faculties/');
    const resProg = await axios.get('/api/users/programs/');
    faculties.value = resFac.data.results || resFac.data;
    faculties.value = faculties.value.map(f => ({
        ...f,
        newProgram: '',
        programs: (resProg.data.results || resProg.data).filter(p => p.faculty === f.id)
    }));
};

const createFaculty = async () => {
    if (!newFacultyName.value) return;
    await axios.post('/api/users/faculties/', { name: newFacultyName.value });
    newFacultyName.value = '';
    fetchFaculties();
};

const createProgram = async (faculty) => {
    if (!faculty.newProgram) return;
    await axios.post('/api/users/programs/', { name: faculty.newProgram, faculty: faculty.id });
    faculty.newProgram = '';
    fetchFaculties();
};

onMounted(fetchFaculties);
</script>